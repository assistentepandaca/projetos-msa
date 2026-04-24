// Quiz Logic
let currentStep = 1;
let totalScore = 0;
let answers = {};
const totalQuestions = 5;

// WhatsApp link for VIP group
const WHATSAPP_LINK = 'https://wa.me/5511997059395?text=Quero%20entrar%20no%20grupo%20VIP%20MSA%20-%20fiz%20o%20quiz';

// Update progress bar
function updateProgress(step) {
    const percentage = Math.round((step / totalQuestions) * 100);
    document.getElementById('progressBar').style.width = percentage + '%';
    document.getElementById('progressPct').textContent = percentage + '%';
    document.getElementById('stepInfo').textContent = `Pergunta ${step} de ${totalQuestions}`;
}

// Select option
function selectOption(button) {
    const question = button.closest('.question');
    const options = question.querySelectorAll('.option');
    
    // Remove previous selection
    options.forEach(opt => opt.classList.remove('selected'));
    
    // Add selection
    button.classList.add('selected');
    
    // Store answer
    const name = button.dataset.name;
    const value = button.dataset.value;
    const points = parseInt(button.dataset.points);
    
    answers[name] = { value, points };
    totalScore += points;
    
    // Move to next question after short delay
    setTimeout(() => {
        if (currentStep < totalQuestions) {
            nextStep();
        } else {
            showResult();
        }
    }, 400);
}

// Next step
function nextStep() {
    const current = document.querySelector(`.question[data-q="${currentStep}"]`);
    current.classList.remove('active');
    
    currentStep++;
    const next = document.querySelector(`.question[data-q="${currentStep}"]`);
    next.classList.add('active');
    
    updateProgress(currentStep);
}

// Show result
function showResult() {
    document.getElementById('quiz-form').style.display = 'none';
    document.querySelector('.progress-section').style.display = 'none';
    
    const resultDiv = document.getElementById('result');
    const contentDiv = document.getElementById('result-content');
    
    let resultHTML = '';
    let ctaText = '';
    let ctaClass = '';
    
    if (totalScore >= 90) {
        resultHTML = `
            <div style="text-align:center; padding: 20px 0;">
                <span style="font-size:60px; display:block; margin-bottom:15px;">🏆</span>
                <h2 style="color: var(--color-text); margin:15px 0;">Você é candidata PERFEITA!</h2>
                <p style="color: var(--color-gold); font-size:18px; font-weight:700;">Score: ${totalScore} pontos</p>
                <p style="color: var(--color-text-muted); margin-top:15px; line-height:1.6;">Seu perfil é <strong>ideal</strong> para o MSA. Você tem todas as características de quem vai ter resultado rápido.</p>
                <div style="background: var(--color-gold-soft); border: 2px solid var(--color-gold); color: var(--color-text); padding:20px; border-radius:12px; margin:20px 0;">
                    <h3 style="color: var(--color-gold); margin-bottom:8px;">🚀 Vaga Garantida no Grupo VIP</h3>
                    <p style="margin:0;">Entre AGORA antes que as vagas acabem!</p>
                </div>
            </div>
        `;
        ctaText = '🔗 ENTRAR NO GRUPO VIP COM PRIORIDADE';
        ctaClass = 'btn-perfect';
    } else if (totalScore >= 75) {
        resultHTML = `
            <div style="text-align:center; padding: 20px 0;">
                <span style="font-size:60px; display:block; margin-bottom:15px;">✅</span>
                <h2 style="color: var(--color-text); margin:15px 0;">Você tem ótimo potencial!</h2>
                <p style="color: var(--color-gold); font-size:18px; font-weight:700;">Score: ${totalScore} pontos</p>
                <p style="color: var(--color-text-muted); margin-top:15px; line-height:1.6;">Seu perfil é <strong>muito bom</strong> para o MSA. Com o método certo, você pode ter resultados em poucas semanas.</p>
                <div style="background: var(--color-gold-soft); border: 2px solid var(--color-gold); color: var(--color-text); padding:20px; border-radius:12px; margin:20px 0;">
                    <h3 style="color: var(--color-gold); margin-bottom:8px;">⚡ Vaga Disponível no Grupo VIP</h3>
                    <p style="margin:0;">Garanta sua vaga antes que acabe!</p>
                </div>
            </div>
        `;
        ctaText = '🔗 ENTRAR NO GRUPO VIP';
        ctaClass = 'btn-good';
    } else if (totalScore >= 55) {
        resultHTML = `
            <div style="text-align:center; padding: 20px 0;">
                <span style="font-size:60px; display:block; margin-bottom:15px;">👍</span>
                <h2 style="color: var(--color-text); margin:15px 0;">Você pode ter resultado!</h2>
                <p style="color: var(--color-gold); font-size:18px; font-weight:700;">Score: ${totalScore} pontos</p>
                <p style="color: var(--color-text-muted); margin-top:15px; line-height:1.6;">Você tem potencial! O MSA pode ser para você, mas precisamos alinhar expectativas. Entre no grupo VIP para conversarmos.</p>
            </div>
        `;
        ctaText = '🔗 ENTRAR NO GRUPO VIP PARA CONVERSAR';
        ctaClass = 'btn-maybe';
    } else {
        resultHTML = `
            <div style="text-align:center; padding: 20px 0;">
                <span style="font-size:60px; display:block; margin-bottom:15px;">💭</span>
                <h2 style="color: var(--color-text); margin:15px 0;">No momento, precisamos conversar</h2>
                <p style="color: var(--color-gold); font-size:18px; font-weight:700;">Score: ${totalScore} pontos</p>
                <p style="color: var(--color-text-muted); margin-top:15px; line-height:1.6;">O MSA exige investimento inicial e dedicação. Entre no grupo VIP que a gente conversa sobre o melhor momento para você começar.</p>
            </div>
        `;
        ctaText = '🔗 ENTRAR NO GRUPO VIP PARA CONVERSAR';
        ctaClass = 'btn-low';
    }
    
    // Add CTA button
    resultHTML += `
        <a href="${WHATSAPP_LINK}" 
           class="cta-button ${ctaClass}" 
           style="display:inline-block; background:linear-gradient(135deg, var(--color-gold) 0%, var(--color-gold-dark) 100%); color:#fff; padding:18px 36px; border-radius:12px; text-decoration:none; font-size:1.1rem; font-weight:800; margin-top:20px; animation:btn-pulse 2s infinite;">
            ${ctaText}
        </a>
        <p style="margin-top:15px; font-size:0.9rem; color:var(--color-text-muted);">⚠️ Só 15 vagas no grupo VIP de pré-lançamento</p>
    `;
    
    contentDiv.innerHTML = resultHTML;
    resultDiv.style.display = 'block';
    
    // Track Meta Pixel event with quiz data
    if (typeof fbq !== 'undefined') {
        fbq('trackCustom', 'QuizCompleted', {
            score: totalScore,
            perfil: answers.perfil?.value || 'unknown',
            barreira: answers.barreira?.value || 'unknown',
            urgencia: answers.urgencia?.value || 'unknown',
            investimento: answers.investimento?.value || 'unknown',
            digital: answers.digital?.value || 'unknown'
        });
        
        fbq('track', 'CompleteRegistration');
    }
    
    // Track GA4 event
    if (typeof gtag !== 'undefined') {
        gtag('event', 'quiz_completed', {
            score: totalScore,
            perfil: answers.perfil?.value || 'unknown',
            barreira: answers.barreira?.value || 'unknown'
        });
    }
    
    // Send data to backend
    submitData();
}

// Submit data
function submitData() {
    const data = {
        score: totalScore,
        answers: answers,
        timestamp: new Date().toISOString(),
        source: window.location.href,
        userAgent: navigator.userAgent
    };
    
    console.log('Quiz data:', data);
    
    // TODO: Replace with your API endpoint
    // fetch('https://your-api.com/quiz', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify(data)
    // });
}

// Event listeners
document.querySelectorAll('.option').forEach(button => {
    button.addEventListener('click', () => selectOption(button));
});

// Initialize
updateProgress(1);
