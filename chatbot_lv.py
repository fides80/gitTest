import pandas as pd
import numpy as np

class SimpleChatBot:
    def __init__(self, filepath):
        self.questions, self.answers = self.load_data(filepath)

    def load_data(self, filepath):
        data = pd.read_csv(filepath)
        questions = data['Q'].tolist()  # 질문열만 뽑아 파이썬 리스트로 저장
        answers = data['A'].tolist()   # 답변열만 뽑아 파이썬 리스트로 저장
        return questions, answers

    def calc_distance(self,a, b):
        ''' 레벤슈타인 거리 계산하기 '''
        if a == b: return 0 # 같으면 0을 반환
        a_len = len(a) # a 길이
        b_len = len(b) # b 길이
        if a == "": return b_len
        if b == "": return a_len

        matrix = [[] for i in range(a_len+1)] # 리스트 컴프리헨션을 사용하여 1차원 초기화
        for i in range(a_len+1): # 0으로 초기화
            matrix[i] = [0 for j in range(b_len+1)]  # 리스트 컴프리헨션을 사용하여 2차원 초기화
        # 0일 때 초깃값을 설정
        for i in range(a_len+1):
            matrix[i][0] = i   # 각 열의 첫번째 값에 0부터 1씩 증가시키며 입력
        for j in range(b_len+1):
            matrix[0][j] = j   # 첫 열을 0부터 1씩 증가시켜 초깃값 입력

        for i in range(1, a_len+1):
            ac = a[i-1]        # a문자열 중 비교할 문자열 선택

            for j in range(1, b_len+1):
                bc = b[j-1]    # b문자열 중 비교할 문자열 선택

                cost = 0 if (ac == bc) else 1  #  문자열이 동일할 경우에는 cost를 0으로 다를 경우는 1로 설정
                matrix[i][j] = min([        # 문자 제거, 삽입, 변경 중 최소값 선택
                    matrix[i-1][j] + 1,     # 문자 제거: 위쪽에서 +1
                    matrix[i][j-1] + 1,     # 문자 삽입: 왼쪽 수에서 +1   
                    matrix[i-1][j-1] + cost # 문자 변경: 대각선에서 +1, 문자가 동일하면 대각선 숫자 복사
                ])

        return matrix[a_len][b_len]         # 최종 계산값 반환
    

    def find_best_answer(self, input_sentence):
        lv=[]                               # 계산값 저장할 빈 리스트 선언
        for i in self.questions:
            x = self.calc_distance(input_sentence,i)   
            lv.append(x)                    # 입력받은 질문과 데이터셋의 질문의 레벤슈타인 거리 계산하여 리스트에 저장

        best_match_index = np.argmin(lv)   # 거리가 가장 가까운 질문의 인덱스를 저장
        return self.answers[best_match_index]   # 거리가 가장 가까운 질문의 대답을 반환

# CSV 파일 경로를 지정하세요.
filepath = 'gitTest\ChatbotData.csv' 

# 간단한 챗봇 인스턴스를 생성합니다.
chatbot = SimpleChatBot(filepath)

# '종료'라는 단어가 입력될 때까지 챗봇과의 대화를 반복합니다.
while True:
    input_sentence = input('You: ')
    if input_sentence.lower() == '종료':
        break
    response = chatbot.find_best_answer(input_sentence)
    print('Chatbot:', response)
    
