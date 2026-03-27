
import torch
from transformers import BertTokenizer, BertModel

DEVICE = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

class BERT():
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.model = BertModel.from_pretrained('bert-base-uncased')
        self.model = self.model.to(DEVICE)
    
    def wordVector(self, word:str) -> torch.Tensor:
        """Get the word embeddings of input word"""
        end_inputs = self.tokenizer(word, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            outputs = self.model(**end_inputs)
        return outputs.last_hidden_state[0, 1, :]
    
    def norm(self, v1:torch.Tensor, v2:torch.Tensor) -> int:
        """Calculate norm of the vector joining v1 and v2"""
        return (torch.linalg.norm(v1 - v2)).item()