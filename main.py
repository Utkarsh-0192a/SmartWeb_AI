from googlesearch import search
import trafilatura
import ollama
from config import logger  # Use shared logger

class websearch:
    def __init__(self):
        self.question = ""
        self.query_gen = """You are a specialized search query generator tasked with producing a precise Google search query to retrieve accurate, authoritative, and up-to-date information in response to a user question.
            Optimize the query for specificity and recency, ensuring it effectively filters out irrelevant results and targets high-quality sources.
            Consider synonyms and contextual nuances to craft a balanced query that maximizes both precision and breadth.
            Your output must be exclusively the query string—no additional text or commentary.
            user question:{}
            output format:
            [query]
        """

        self.sel_url = """
            You are an expert research assistant and expert in analysis. You are given 10 URLs, each with a title and description.
            Evaluate the titles and descriptions to select the URL that are most relevant and authoritative for answering the user's question.
            so that from the context provided by these URL, any one can craft a detailed, accurate, and comprehensive answer to the user's question.
            Output only the final answer along with the two selected URLs, with no extra commentary.
            user question:{}
            urls and tiltle , description:
            {}
            output format:
            selected_url1
            selected_url2
            """

        self.answer_gen = """
            You are a sophisticated AI language model trained to generate detailed, accurate, and comprehensive answers to complex questions.
            Given the context and the user question, craft a detailed, accurate, and comprehensive answer.
            Your answer should be informative, well-structured, and tailored to the user's question.
            Avoid irrelevant information and focus on providing a clear and concise response.
            Your output must be exclusively the answer text—no additional text or commentary.
            make sure answer should not be short and should be detailed.
            user question:{}
            context:
            {}
            output format:
            [answer]
            """
        logger.info("Websearch instance created.")

    # def set_question(self, question):
    #     self.question = question

    def get_result(self):
        logger.info(f"Getting search results for question: {self.question}")
        try:
            p = search(self.question, sleep_interval=5, num_results=5, advanced=True)
            data = []
            for i in p:
                tmp = {
                    "url": i.url,
                    "title": i.title,
                    "description": i.description
                }
                data.append(tmp)

            promp = self.sel_url.format(self.question, data)
            
            urls = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": promp}])
            urls = urls['message']['content']
            urls = urls.split('\n')
            urls = [i for i in urls if i.startswith("http")]
            logger.info(f"Selected URLs: {urls}")
            return urls
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return []

    def get_content(self):
        try:
            url = self.get_result()[0]
            logger.info(f"Getting resource from {url}")
            downloaded = trafilatura.fetch_url(url)
            result = trafilatura.extract(downloaded)
            logger.info("Content extracted successfully.")
            return result
        except Exception as e:
            logger.error(f"Error during content extraction: {e}")
            return ""

    def get_answer(self, question):
        self.question = question
        try:
            context = self.get_content()
            promp = self.answer_gen.format(self.question, context)
            answer = ollama.chat(model="llama3.2", messages=[{"role": "user", "content": promp}])
            logger.info("Answer generated successfully.")
            return answer['message']['content']
        except Exception as e:
            logger.error(f"Error during answer generation: {e}")
            return "An error occurred while generating the answer."
    
    def get_prompt(self, question):
        self.question = question
        try:
            context = self.get_content()
            logger.info("Content extracted for prompt generation.")
            print("generated the prompt")
            return self.answer_gen.format(self.question, context)
        except Exception as e:
            logger.error(f"Error during prompt generation: {e}")
            return ""

# Example usage:
if __name__ == "__main__":
    searcher = websearch()
    question = input("Enter your question: ")
    answer = searcher.get_answer(question)
    print(answer)

