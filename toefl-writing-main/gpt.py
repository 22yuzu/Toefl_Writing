import openai
import os

def generate_question():
    try:
        response = openai.Completion.create(
          engine="text-davinci-003",
          prompt="Generate a TOEFL independent writing task question.",
          temperature=0.6,
          max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        print(f"Error generating question: {str(e)}")
        raise e

def score_answer(answer, question):
    try:
        # generate feedback
        feedback_prompt = f"The following TOEFL essay was submitted:\n\n{answer}\n\nPlease provide feedback and errors:"
        feedback_response = openai.Completion.create(
          engine="text-davinci-003",
          prompt=feedback_prompt,
          temperature=0.6,
          max_tokens=100
        )
        print(f"answer: {answer}")
        feedback = feedback_response.choices[0].text.strip()

        # generate sample answer
        sample_answer_prompt = f"The question was: {question}\n\nGenerate a high-quality TOEFL essay about 300 words in response to the same question."
        sample_answer_response = openai.Completion.create(
          engine="text-davinci-003",
          prompt=sample_answer_prompt,
          temperature=0.6,
          max_tokens=600  # 300 words?
        )
        sample_answer = sample_answer_response.choices[0].text.strip()

        # generate a score
        score_prompt = f"The following TOEFL essay was submitted:\n\n{answer}\n\nPlease score this essay on a scale of 1-30 based on grammar, vocabulary, length(about 300 words is good), structure, persuasiveness, etc.:"
        score_response = openai.Completion.create(
          engine="text-davinci-003",
          prompt=score_prompt,
          temperature=0.6,
          max_tokens=10
        )
        
        try:
            score_text = score_response.choices[0].text.strip()
            score = int(score_text)
        except ValueError:
            score = None

        return score, feedback, sample_answer
    except Exception as e:
        print(f"Error scoring answer: {str(e)}")
        raise e
