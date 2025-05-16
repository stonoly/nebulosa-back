import spacy
from .models import Tag

class TagSearchService:
    def __init__(self):
        # Initialize the NLP model to process the keyword in French
        self.nlp_model = spacy.load("fr_core_news_md")
    
    def search_similar_tags(self, keyword):
        """
        Search for tags similar to a keyword using semantic similarity.
        
        Args:
            keyword (str): The keyword to search for
            
        Returns:
            dict: A dictionary of tag names and their similarity scores
        """
        # Convert the keyword to a semantic vector
        keyword_vector = self.nlp_model(keyword)
        similarity_scores = {}

        existing_tags = Tag.objects.all()
        for tag in existing_tags:
            tag_vector = self.nlp_model(tag.name)

            # Calculate the similarity score (between 0 and 1)
            similarity_score = keyword_vector.similarity(tag_vector)
            similarity_scores[tag.name] = similarity_score
            
        # Return the results sorted by decreasing similarity score
        return dict(
            sorted(
                similarity_scores.items(),
                key=lambda item: item[1],
                reverse=True
            )
        ) 