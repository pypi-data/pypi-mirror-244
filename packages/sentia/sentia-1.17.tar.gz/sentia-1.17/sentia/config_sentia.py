from transformers import LlamaConfig

SENTIA_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    "Locutusque/sentia-xs": "https://huggingface.co/Locutusque/sentia-xs/resolve/main/config.json",
}

class SENTIAConfig(LlamaConfig):
    model_type = "sentia"

    def __init__(
        self, 
        vocab_size=65027,
        hidden_dim=512,
        n_embed=512,
        n_layer=12,
        n_head=16,
        n_inner=2048,
        memory_strength=5,
        pdrop = 0.0,
        cross_attention=False,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.vocab_size = vocab_size
        self.memory_strength = memory_strength
        self.hidden_dim = hidden_dim
        self.hidden_size = hidden_dim
        self.n_embd = n_embed
        self.n_layer = n_layer
        self.num_attention_heads = n_head
        self.num_hidden_layers = n_layer
        self.intermediate_size = n_inner
        self.pad_token_id = kwargs.pop("pad_token_id", None)
        self.decoder_start_token_id = kwargs.pop("decoder_start_token_id", self.pad_token_id)
        self.max_position_embeddings = n_inner
        self.num_key_value_heads = n_head
        self.num_hidden_layers = n_layer
        self.n_head = n_head
        self.bad_words_ids = None
        self.n_inner = n_inner
        self.pdrop = pdrop
        self.add_cross_attention = cross_attention