import torch
from transformers import BertTokenizer, BertModel

DEVICE = torch.device('mps' if torch.backends.mps.is_available() else 'cpu')

class BERT():
    def __init__(self, path):
        self.tokenizer = BertTokenizer.from_pretrained(path)
        self.model = BertModel.from_pretrained(path)
        self.model = self.model.to(DEVICE)
    
    def wordVector(self, word:str) -> torch.Tensor:
        """Get the word embeddings of input word"""
        end_inputs = self.tokenizer(word, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            outputs = self.model(**end_inputs)
        return outputs.last_hidden_state[0, 1, :]
    
    def cos_sim(self, v1:torch.Tensor, v2:torch.Tensor) -> int:
        """Calculate cosine_similarity of the vector joining v1 and v2"""
        return (torch.nn.functional.cosine_similarity(v1, v2, dim=0)).item()
    
if __name__ == "__main__":
    save_path = "./model_weights"
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    tokenizer.save_pretrained(save_path)
    model.save_pretrained(save_path)