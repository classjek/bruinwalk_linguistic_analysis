# from pysentimiento import create_analyzer
# import csv

# reviews = []
# with open('./bertweet-sentiment-analysis/revs.csv', 'r') as f:
#     reader = csv.reader(f)
#     next(reader)
#     for row in reader:
#         reviews.append(row[5])


# print("finished initializing reviews")

# sentiment_analyzer = create_analyzer(task="sentiment", lang="en")
# emotion_analyzer = create_analyzer(task="emotion", lang="en")

# for review in reviews:
#     print(sentiment_analyzer.predict(review))
#     print(emotion_analyzer.predict(review))

from pysentimiento import create_analyzer
import csv

reviews = []
with open('./bertweet-sentiment-analysis/review_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        reviews.append(row[5])

sentiment_analyzer = create_analyzer(task="sentiment", lang="en")

with open('./bertweet-sentiment-analysis/sentiment_data.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['prof', 'gender', 'class', 'reviewer', 'review_grade', 'review_text', 'sentiment'])
    for review in reviews:
        sentiment_output = sentiment_analyzer.predict(review)
        sentiment = str(sentiment_output).replace("AnalyzerOutput(output=POS, probas={", "").replace("AnalyzerOutput(output=NEG, probas={", "").replace("AnalyzerOutput(output=NEU, probas={", "").replace("})", "")

        writer.writerow(['professor name', 'gender', 'class name', 'reviewer name', 'review grade', review, sentiment])

print("finished writing sentiment analysis results to file")

