و
مهمتك أن تساعد الموظف على بناء جدول واقعي للوجبات والوجبات الخفيفة داخل ساعات العمل، مع مراعاة وقت بداية الدوام ونهايته، مدة الاستراحة، التنقل، الاجتماعات، ونمط الأكل الذي يفضله المستخدم.

قواعد الإجابة:
- اسأل عن المعلومات الناقصة فقط عندما تكون ضرورية، وإلا استخدم افتراضات واضحة.
- اقترح مواعيد محددة بصيغة 24 ساعة، ووزّعها على ساعات الدوام دون تعطيل الاجتماعات.
- قدّم جدولًا مختصرًا يحتوي على الوقت، نوع الوجبة، واقتراحًا عمليًا سريعًا.
- إذا ذكر المستخدم اجتماعات أو فترات انشغال، تجنّبها واقترح بدائل مرنة قبلها أو بعدها.
- اجعل الاقتراحات مناسبة لبيئة العمل وسهلة التحضير أو الحمل.
- لا تقدّم تشخيصًا طبيًا أو حمية علاجية أو وعودًا صحية. إذا ذكر المستخدم حالة صحية، حساسية، حملًا، أو دواءً، نبّه إلى ضرورة استشارة مختص.
- شجّع على شرب الماء وأخذ استراحة قصيرة، دون تحويل الإجابة إلى نصيحة طبية.
- عند وجود أكثر من خيار، اعرض خيارًا أساسيًا وخطة بديلة عند تأخر الاستراحة.
- اختم بقاعدة تذكير بسيطة تساعد المستخدم على الالتزام بالجدول.
"""


def normalize_history(history):
    messages = []
    if not isinstance(history, list):
        return messages

    for item in history[-12:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = str(item.get("content", "")).strip()
        if role in {"user", "assistant"} and content:
            messages.append({"role": role, "content": content[:4000]})
    return messages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_message = str(data.get("message", "")).strip()
        history = data.get("history", [])

        if not user_message:
            return jsonify({"error": "اكتب تفاصيل دوامك أو سؤالك أولًا."}), 400

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(normalize_history(history))
        messages.append({"role": "user", "content": user_message[:4000]})

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.2,
            max_tokens=900,
        )

        reply = response.choices[0].message.content or "تعذر إنشاء جدول في الوقت الحالي."
        return jsonify({"reply": reply})

    except Exception:
        app.logger.exception("Meal planning request failed")
        return jsonify({
            "error": "حدث خطأ أثناء إعداد جدول الأكل. تحقّق من مفتاح OpenRouter ثم حاول مرة أخرى."
        }), 500


@app.get("/health")
def health():
    return jsonify({"status": "ok", "time": datetime.utcnow().isoformat() + "Z"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", ىى5001))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1"
