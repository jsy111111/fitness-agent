import openai
import os
from dotenv import load_dotenv

load_dotenv()

def generate_workout_routine():
    print("--- 🏋️ 오늘의 운동 루틴 가이드 에이전트 ---\n")
    
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    while True:
        try:
            duration = int(input("운동 가능 시간(분 단위, 예: 20): "))
            if duration < 5:
                print("❌ 최소 5분 이상 입력해주세요.\n")
                continue
            break
        except ValueError:
            print("❌ 숫자로 입력해주세요.\n")
    
    target_body_part = input("집중하고 싶은 부위(예: 하체, 상체, 전신): ").strip()
    equipment = input("도구 유무(예: 없음, 덤벨, 밴드): ").strip()
    
    if not target_body_part or not equipment:
        print("❌ 모든 입력값을 채워주세요.")
        return

    system_instruction = f"""
당신은 전문 퍼스널 트레이너 '루틴 마스터'입니다. 
사용자의 제약 사항을 분석하여 1분 단위의 정교한 운동 스케줄을 작성합니다.

[규칙]
1. 전체 시간 {duration}분에 맞춰 웜업(2분), 메인 운동, 쿨다운(2분)을 배정하세요.
2. 부위: {target_body_part}, 도구: {equipment} 조건을 반드시 반영하세요.
3. '타임라인 | 운동명 | 세트/횟수 | 주의사항' 형식의 테이블이나 리스트로 출력하세요.
4. 친절하고 파이팅 넘치는 톤으로 작성하세요.
5. 초보자도 따라할 수 있는 명확한 지시사항 제공.
"""

    user_message = f"시간: {duration}분, 부위: {target_body_part}, 도구: {equipment}. 최적의 루틴을 짜줘."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7
        )

        print("\n" + "="*50)
        print("✨ 생성된 맞춤형 운동 루틴입니다 ✨")
        print("="*50)
        print(response.choices[0].message.content)
        print("="*50 + "\n")
        
        while True:
            feedback = input("루틴에 대해 추가 요청사항이 있으신가요? (예: 더 쉽게/어렵게/더 짧게) 또는 'q'를 입력해 종료: ").strip()
            
            if feedback.lower() == 'q':
                print("\n감사합니다! 좋은 운동되세요! 💪")
                break
            
            if not feedback:
                continue
            
            follow_up_response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": user_message},
                    {"role": "assistant", "content": response.choices[0].message.content},
                    {"role": "user", "content": f"요청: {feedback}"}
                ],
                temperature=0.7
            )
            
            print("\n" + "="*50)
            print("✨ 수정된 운동 루틴입니다 ✨")
            print("="*50)
            print(follow_up_response.choices[0].message.content)
            print("="*50 + "\n")

    except Exception as e:
        print(f"❌ 오류가 발생했습니다: {e}")

if __name__ == "__main__":
    generate_workout_routine()