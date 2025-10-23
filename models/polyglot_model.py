# models/polyglot_model.py
import torch
import torch.nn as nn
from transformers import PreTrainedModel, PretrainedConfig
import json

class PolyglotTutorConfig(PretrainedConfig):
    model_type = "polyglot_tutor"
    
    def __init__(
        self,
        vocab_size=20000,
        hidden_size=128,
        num_hidden_layers=4,
        num_attention_heads=4,
        intermediate_size=384,
        max_position_embeddings=256,
        num_languages=3,
        num_subjects=8,
        **kwargs
    ):
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.intermediate_size = intermediate_size
        self.max_position_embeddings = max_position_embeddings
        self.num_languages = num_languages
        self.num_subjects = num_subjects
        super().__init__(**kwargs)

class TinySelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.num_attention_heads = config.num_attention_heads
        self.hidden_size = config.hidden_size
        self.attention_head_size = self.hidden_size // self.num_attention_heads
        self.all_head_size = self.num_attention_heads * self.attention_head_size

        self.query = nn.Linear(config.hidden_size, self.all_head_size)
        self.key = nn.Linear(config.hidden_size, self.all_head_size)
        self.value = nn.Linear(config.hidden_size, self.all_head_size)
        self.dropout = nn.Dropout(0.1)

    def transpose_for_scores(self, x):
        new_x_shape = x.size()[:-1] + (self.num_attention_heads, self.attention_head_size)
        x = x.view(new_x_shape)
        return x.permute(0, 2, 1, 3)

    def forward(self, hidden_states, attention_mask=None):
        query_layer = self.transpose_for_scores(self.query(hidden_states))
        key_layer = self.transpose_for_scores(self.key(hidden_states))
        value_layer = self.transpose_for_scores(self.value(hidden_states))

        attention_scores = torch.matmul(query_layer, key_layer.transpose(-1, -2))
        attention_scores = attention_scores / (self.attention_head_size ** 0.5)
        
        if attention_mask is not None:
            attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)
            attention_scores = attention_scores + attention_mask

        attention_probs = nn.functional.softmax(attention_scores, dim=-1)
        attention_probs = self.dropout(attention_probs)

        context_layer = torch.matmul(attention_probs, value_layer)
        context_layer = context_layer.permute(0, 2, 1, 3).contiguous()
        new_context_layer_shape = context_layer.size()[:-2] + (self.all_head_size,)
        context_layer = context_layer.view(new_context_layer_shape)
        
        return context_layer

class TinySelfOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=1e-12)
        self.dropout = nn.Dropout(0.1)

    def forward(self, hidden_states, input_tensor):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = self.LayerNorm(hidden_states + input_tensor)
        return hidden_states

class TinyAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.self = TinySelfAttention(config)
        self.output = TinySelfOutput(config)
        
    def forward(self, hidden_states, attention_mask=None):
        self_output = self.self(hidden_states, attention_mask)
        attention_output = self.output(self_output, hidden_states)
        return attention_output

class TinyIntermediate(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.hidden_size, config.intermediate_size)
        self.intermediate_act_fn = nn.GELU()

    def forward(self, hidden_states):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.intermediate_act_fn(hidden_states)
        return hidden_states

class TinyOutput(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.dense = nn.Linear(config.intermediate_size, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size, eps=1e-12)
        self.dropout = nn.Dropout(0.1)

    def forward(self, hidden_states, input_tensor):
        hidden_states = self.dense(hidden_states)
        hidden_states = self.dropout(hidden_states)
        hidden_states = self.LayerNorm(hidden_states + input_tensor)
        return hidden_states

class TinyTransformerLayer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.attention = TinyAttention(config)
        self.intermediate = TinyIntermediate(config)
        self.output = TinyOutput(config)
        
    def forward(self, hidden_states, attention_mask=None):
        attention_output = self.attention(hidden_states, attention_mask)
        intermediate_output = self.intermediate(attention_output)
        layer_output = self.output(intermediate_output, attention_output)
        return layer_output

class EfficientTransformer(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.layer = nn.ModuleList([TinyTransformerLayer(config) for _ in range(config.num_hidden_layers)])

    def forward(self, hidden_states, attention_mask=None):
        for layer_module in self.layer:
            hidden_states = layer_module(hidden_states, attention_mask)
        return hidden_states

class MultilingualEmbeddings(nn.Module):
    def __init__(self, config):
        super().__init__()
        self.word_embeddings = nn.Embedding(config.vocab_size, config.hidden_size)
        self.position_embeddings = nn.Embedding(config.max_position_embeddings, config.hidden_size)
        self.language_embeddings = nn.Embedding(config.num_languages, config.hidden_size)
        self.LayerNorm = nn.LayerNorm(config.hidden_size)
        self.dropout = nn.Dropout(0.1)
        
    def forward(self, input_ids, language_id=None):
        seq_length = input_ids.size(1)
        position_ids = torch.arange(seq_length, dtype=torch.long, device=input_ids.device)
        
        word_emb = self.word_embeddings(input_ids)
        pos_emb = self.position_embeddings(position_ids).unsqueeze(0)
        
        embeddings = word_emb + pos_emb
        
        if language_id is not None:
            lang_emb = self.language_embeddings(language_id).unsqueeze(1)
            embeddings += lang_emb
        
        embeddings = self.LayerNorm(embeddings)
        return self.dropout(embeddings)

class PolyglotTutorModel(PreTrainedModel):
    config_class = PolyglotTutorConfig
    
    def __init__(self, config):
        super().__init__(config)
        self.embeddings = MultilingualEmbeddings(config)
        self.encoder = EfficientTransformer(config)
        self.language_head = nn.Linear(config.hidden_size, config.num_languages)
        self.subject_head = nn.Linear(config.hidden_size, config.num_subjects)
        self.answer_head = nn.Linear(config.hidden_size, config.vocab_size)
        
    def forward(self, input_ids, attention_mask=None, language_id=None):
        embeddings = self.embeddings(input_ids, language_id)
        encoded = self.encoder(embeddings, attention_mask)
        
        language_logits = self.language_head(encoded[:, 0])
        subject_logits = self.subject_head(encoded[:, 0])
        answer_logits = self.answer_head(encoded)
        
        return {
            'language_logits': language_logits,
            'subject_logits': subject_logits,
            'answer_logits': answer_logits
        }
