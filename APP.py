
<!doctype html>
<html lang="ar" dir="rtl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>منظّم الأكل أثناء الدوام</title>
  <style>
    :root { font-family: Arial, sans-serif; color: #172033; background: #f4f7fb; }
    * { box-sizing: border-box; }
    body { margin: 0; }
    .container { max-width: 920px; margin: 0 auto; padding: 32px 16px; }
    .card { background: white; border-radius: 18px; padding: 24px; margin-bottom: 18px; box-shadow: 0 8px 24px rgba(30, 50, 80, .08); }
    h1 { margin: 0 0 10px; color: #0f766e; }
    p { line-height: 1.8; }
    .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; }
    label { display: block; font-weight: bold; margin-bottom: 6px; }
    input, textarea, button { width: 100%; border: 1px solid #d7deea; border-radius: 10px; padding: 12px; font: inherit; }
    textarea { min-height: 130px; resize: vertical; }
    button { border: 0; background: #0f766e; color: white; cursor: pointer; font-weight: bold; margin-top: 14px; }
    button:hover { background: #115e59; }
    .hint { color: #5b6577; font-size: .94rem; }
    .motivation { background: #ecfdf5; color: #047857; border-right: 4px solid #10b981; padding: 12px 14px; border-radius: 8px; font-weight: bold; }
    #result { white-space: pre-wrap; line-height: 1.9; }
    .error { color: #b42318; }
    .loading { color: #0f766e; }
  </style>
</head>
<body>
  <main class="container">
    <section class="card">
      <h1>منظّم الأكل أثناء الدوام</h1>
      <p>أدخل أوقات عملك والتزاماتك اليومية، وسيقترح لك المساعد جدولًا عمليًا للوجبات والوجبات الخفيفة يناسب دوامك.</p>

      <div class="grid">
        <div>
          <label for="start">بداية الدوام</label>
          <input id="start" type="time" value="08:00">
        </div>
        <div>
          <label for="end">نهاية الدوام</label>
          <input id="end" type="time" value="17:00">
        </div>
        <div>
          <label for="break">مدة الاستراحة بالدقائق</label>
          <input id="break" type="number" min="5" value="30">
        </div>
      </div>

      <p id="motivation" class="motivation">خطوة صغيرة اليوم تصنع عادة أسهل غدًا.</p>
      <p class="hint">مثال على الاجتماعات: اجتماع يومي 09:00–09:30، واجتماعات متواصلة من 13:00 إلى 15:00.</p>
      <textarea id="details" placeholder="اكتب الاجتماعات، وقت الاستيقاظ، الوجبة التي تفضلها، وهل تحتاج وجبات خفيفة..."></textarea>
      <button id="submit">أنشئ جدول الأكل</button>
    </section>

    <section class="card">
      <h2>الاقتراح</h2>
      <div id="result" class="hint">سيظهر جدولك هنا.</div>
    </section>
  </main>

  <script>
    const history = [];
    const motivation = document.getElementById('motivation');
    const result = document.getElementById('result');
    const button = document.getElementById('submit');
    const motivationalPhrases = [
      'خطوة صغيرة اليوم تصنع عادة أسهل غدًا.',
      'نظّم وقت وجبتك، واترك لطاقتك مساحة أفضل.',
      'الاستمرارية أهم من المثالية؛ ابدأ بالوقت المتاح.',
      'استراحة قصيرة ومنظمة قد تغيّر إيقاع يومك.',
      'كل وجبة مخططة هي قرار واحد أقل تحت ضغط الدوام.'
    ];

    function showRandomMotivation() {
      motivation.textContent = motivationalPhrases[Math.floor(Math.random() * motivationalPhrases.length)];
    }

    showRandomMotivation();

    button.addEventListener('click', async () => {
      const start = document.getElementById('start').value;
      const end = document.getElementById('end').value;
      const breakMinutes = document.getElementById('break').value;
      const details = document.getElementById('details').value.trim();

      if (!start || !end) {
        result.className = 'error';
        result.textContent = 'حدد بداية الدوام ونهايته.';
        return;
      }

      const message = `دوامي من ${start} إلى ${end}. مدة الاستراحة المتاحة ${breakMinutes} دقيقة. تفاصيل إضافية: ${details || 'لا توجد تفاصيل إضافية.'}`;
      result.className = 'loading';
      result.textContent = 'جارٍ إعداد جدول مناسب...';
      button.disabled = true;

      try {
        const response = await fetch('/api/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message, history })
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'تعذر الاتصال بالخادم.');
        history.push({ role: 'user', content: message });
        history.push({ role: 'assistant', content: data.reply });
        result.className = '';
        result.textContent = data.reply;
        showRandomMotivation();
      } catch (error) {
        result.className = 'error';
        result.textContent = error.message;
      } finally {
        button.disabled = false;
      }
    });
  </script>
</body>
</html>
