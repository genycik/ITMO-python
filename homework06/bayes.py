from collections import Counter
import math


class NaiveBayesClassifier:

    def __init__(self, alpha=1):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        labeled_words_lst = []
        for sentence, label in zip(X, y):
            for word in sentence.split():
                labeled_words_lst.append((word, label))
        self.labeled_words = Counter(labeled_words_lst)

        self.words_num = dict(
            Counter([word for sentence in X for word in sentence.split()]))

        self.labeles_num = dict(Counter(y))

        self.model = {
        'words': {},
        'labels': {}
        }

        for label in self.labeles_num:
            params = {
            'num_words_with_label': self.count_words_with_labeles(label),
            'likelihood': self.labeles_num[label] / len(y)
            }

            self.model['labels'][label] = params

        for word in self.words_num:
            params = {}

            for label in self.labeles_num:

                params[label] = self.smoothing_likelihood(word, label)

            self.model['words'][word] = params


    def count_words_with_labeles(self, cur_label):

        num = 0

        for word, label_name in self.labeled_words:
            if cur_label == label_name:
                num += self.labeled_words[(word, cur_label)]

        return num


    def smoothing_likelihood(self, word, cur_label):

        nc = self.model['labels'][cur_label]['num_words_with_label']
        nic = self.labeled_words.get((word, cur_label), 0)
        d = len(self.words_num)
        alpha = self.alpha

        return (nic + alpha) / (nc + alpha * d)



    def predict(self, X):
        """ Perform labelification on an array of test vectors X. """
        for sentence in X:
            words = sentence.split()
            likely_labels = []

            for cur_label in self.model['labels']:

                likelihood = self.model['labels'][cur_label]['likelihood']

                
                total_score = math.log(likelihood, math.e)

                for word in words:
                    word_dict = self.model['words'].get(word, None)

                    if word_dict:
                        
                        total_score += math.log(word_dict[cur_label], math.e)

                likely_labels.append((total_score, cur_label))

           
            _, answer = max(likely_labels)

        return answer


    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        count = len(y_test)
        correct = 0
        for i, answer in enumerate(self.predict(X_test)):
            if answer == y_test[i]:
                correct += 1

        return correct / count
