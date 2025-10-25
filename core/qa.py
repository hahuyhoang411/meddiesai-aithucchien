import base64
from openai import OpenAI

from .settings import settings

client = OpenAI(api_key=settings.ATC_API_KEY, base_url=settings.ATC_BASE_URL)


system_prompt = """
Your are a designer expert.
"""
prompt = """
You will need to design a marketing campaign for the Lunar New Year 2026, focusing on promoting the main product "Techcombank Sinh lời tự động".

- Task:
Thiết kế chiến dịch marketing sáng tạo cho mùa Tết 2026, nhằm quảng bá sản phẩm chủ lực “Techcombank Sinh lời tự động”.
Chiến dịch cần thể hiện tinh thần Tết – thời điểm của khởi đầu, tài lộc và sum vầy – đồng thời truyền tải giá trị cốt lõi (CVP) của “Techcombank Sinh lời tự động” một cách gần gũi, dễ hiểu và phù hợp với khách hàng Việt Nam.
Bản ý tưởng chiến dịch ngắn gọn (tối đa 10 slide hoặc 10 trang A4) bao gồm hình ảnh, khẩu hiệu, hành trình khách hàng, hoặc mẫu quảng cáo minh họa,...
Sản phẩm là hoàn toàn sáng tạo mới với AI thông qua AI API được cung cấp, đáp ứng đủ yêu cầu của đề, phù hợp quy định pháp lý và giáo dục, không cover hay sáng tác từ một sản phẩm có sẵn
Đầu ra: File PPTX/PDF/DOCX
Ngôn ngữ: tiếng Việt
Tham khảo thông tin sản phẩm và nhận diện thương hiệu tại https://techcombank.com/"""


response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": prompt,
        },
    ],
)

print(response.choices[0].message.content)
