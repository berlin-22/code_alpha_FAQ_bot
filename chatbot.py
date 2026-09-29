import torch
from sentence_transformers import SentenceTransformer, util
from faq_data import FAQ_DATA


class FAQChatbot:
    """
    FAQ Chatbot using local sentence-transformers (all-MiniLM-L6-v2)
    and dense cosine similarity for true semantic matching.
    Runs 100% locally on CPU/GPU without external API keys.
    """

    def __init__(self, high_threshold: float = 0.50, low_threshold: float = 0.35):
        """
        Initialize the chatbot with the local embedding model and FAQ data.

        Args:
            high_threshold: Minimum score to return a direct confident answer.
            low_threshold: Minimum score to consider related questions.
        """
        self.high_threshold = high_threshold
        self.low_threshold = low_threshold
        self.faq_data = FAQ_DATA
        self.questions = [faq["question"] for faq in self.faq_data]
        self.answers = [faq["answer"] for faq in self.faq_data]

        # Use CPU explicitly for consistent zero-conflict inference
        self.device = "cpu"
        self.model = SentenceTransformer("all-MiniLM-L6-v2", device=self.device)

        # Pre-compute embeddings for all FAQ questions
        self.faq_embeddings = self.model.encode(
            self.questions,
            convert_to_tensor=True,
            device=self.device,
            show_progress_bar=False,
        )

    def get_response(self, user_query: str) -> dict:
        """
        Find the best matching FAQ answer for a user query.
        Handles direct matches, ambiguous related policies, and out-of-domain queries.
        """
        if not user_query or not user_query.strip():
            return {
                "answer": "Please type a question so I can help you.",
                "matched_question": None,
                "confidence": 0.0,
                "top_matches": [],
                "status": "empty",
            }

        query_clean = user_query.strip()
        query_embedding = self.model.encode(
            query_clean,
            convert_to_tensor=True,
            device=self.device,
            show_progress_bar=False,
        )

        similarity_tensor = util.cos_sim(query_embedding, self.faq_embeddings)[0]
        similarities = similarity_tensor.cpu().numpy()

        top_indices = similarities.argsort()[-3:][::-1]
        top_matches = [
            {
                "question": self.questions[i],
                "answer": self.answers[i],
                "score": float(similarities[i]),
            }
            for i in top_indices
        ]

        best_idx = int(similarities.argmax())
        best_score = float(similarities[best_idx])

        # Case 1: High confidence direct match
        if best_score >= self.high_threshold:
            return {
                "answer": self.answers[best_idx],
                "matched_question": self.questions[best_idx],
                "confidence": best_score,
                "top_matches": top_matches,
                "status": "matched",
            }

        # Case 2: Ambiguous / borderline match (e.g., asked about 'leave policy' matching 'return policy')
        elif best_score >= self.low_threshold:
            suggestions = "\n".join([f"- **{m['question']}**" for m in top_matches if m["score"] >= self.low_threshold])
            return {
                "answer": (
                    f"I'm not sure if you are asking about one of our store policies. Did you mean:\n\n"
                    f"{suggestions}\n\n"
                    f"*(Please rephrase or click a specific question above)*"
                ),
                "matched_question": None,
                "confidence": best_score,
                "top_matches": top_matches,
                "status": "clarify",
            }

        # Case 3: Out of domain / no match
        else:
            return {
                "answer": (
                    "I couldn't find a matching FAQ for that question. "
                    "Our support covers shipping, returns, orders, payments, and account settings. "
                    "Could you please rephrase your query?"
                ),
                "matched_question": None,
                "confidence": best_score,
                "top_matches": [],
                "status": "unmatched",
            }

    def get_all_questions(self) -> list[str]:
        return self.questions

    def get_categories(self) -> dict[str, list[str]]:
        categories = {
            "Shipping & Delivery": [],
            "Payments & Pricing": [],
            "Returns & Refunds": [],
            "Account Management": [],
            "Orders & Tracking": [],
            "General Questions": [],
        }

        keyword_map = {
            "Shipping & Delivery": ["ship", "delivery", "deliver", "transit", "track"],
            "Payments & Pricing": ["pay", "price", "discount", "installment", "cash", "cod", "cost"],
            "Returns & Refunds": ["return", "refund", "exchange", "damage", "warranty"],
            "Account Management": ["account", "password", "email", "unsubscribe", "delete", "sign up", "login"],
            "Orders & Tracking": ["order", "cancel", "modify", "bulk", "wholesale"],
        }

        for q in self.questions:
            q_lower = q.lower()
            categorized = False
            for cat, keywords in keyword_map.items():
                if any(kw in q_lower for kw in keywords):
                    categories[cat].append(q)
                    categorized = True
                    break
            if not categorized:
                categories["General Questions"].append(q)

        return {k: v for k, v in categories.items() if v}
