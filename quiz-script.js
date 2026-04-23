// Quiz Logic
let currentStep = 1;
let totalScore = 0;
let answers = {};
const totalQuestions = 5;

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
    }, 300);
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
    
    if (totalScore >= 90) {
        resultHTML = `
            <div style="text-align:center;">
                <span style="font-size:60px;">🏆</span>
                <h2 style="color:#2d3748; margin:15px 0;">Você é candidata PERFEITA!</h2>
                <p style="color:#667eea; font-size:18px; font-weight:600;">Score: ${totalScore} pontos</p>
                <p style="color:#4a5568; margin-top:15px;">Seu perfil é ideal para o MSA. Vou te ligar em breve para conversarmos!</p>
                <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; padding:20px; border-radius:12px; margin:20px 0;">
                    <h3>🚀 Grupo VIP - Prioridade Máxima</h3>
                    <p>Vaga garantida. Entre agora!</p>
                </div>
            </div>
        `;
    } else if (totalScore >= 75) {
        resultHTML = `
            <div style="text-align:center;">
                <span style="font-size:60px;">✅</span>
                <h2 style="color:#2d3748; margin:15px 0;">Você tem ótimo potencial!</h2>
                <p style="color:#667eea; font-size:18px; font-weight:600;">Score: ${totalScore} pontos</p>
                <p style="color:#4a5568; margin-top:15px;">Seu perfil é muito bom para o MSA. Com o método certo, você pode ter resultados rápidos!</p>
                <div style="background:linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:white; padding:20px; border-radius:12px; margin:20px 0;">
                    <h3>⚡ Vaga disponível no Grupo VIP</h3>
                    <p>Garanta sua vaga antes que acabe!</p>
                </div>
            </div>
        `;
    } else if (totalScore >= 55) {
        resultHTML = `
            <div style="text-align:center;">
                <span style="font-size:60px;">👍</span>
                <h2 style="color:#2d3748; margin:15px 0;">Você pode ter resultado!</h2>
                <p style="color:#667eea; font-size:18px; font-weight:600;">Score: ${totalScore} pontos</p>
                <p style="color:#4a5568; margin-top:15px;">Você tem potencial, mas precisamos conversar sobre expectativas e timing.</p>
                <div style="background:#718096; color:white; padding:20px; border-radius:12px; margin:20px 0;">
                    <h3>📧 Lista de Espera</h3>
                    <p>Entraremos em contato em breve!</p>
                </div>
            </div>
        `;
    } else {
        resultHTML = `
            <div style="text-align:center;">
                <span style="font-size:60px;">💭</span>
                <h2 style="color:#2d3748; margin:15px 0;">No momento não é pra você</h2>
                <p style="color:#667eea; font-size:18px; font-weight:600;">Score: ${totalScore} pontos</p>
                <p style="color:#4a5568; margin-top:15px;">O MSA exige investimento em anúncios e dedicação. Quando você tiver condições, estaremos aqui!</p>
                <div style="background:#a0aec0; color:white; padding:20px; border-radius:12px; margin:20px 0;">
                    <h3>📚 Conteúdo Gratuito</h3>
                    <p>Te enviaremos dicas por e-mail!</p>
                </div>
            </div>
        `;
    }
    
    contentDiv.innerHTML = resultHTML;
    resultDiv.style.display = 'block';
    
    // Track event
    if (typeof fbq !== 'undefined') {
        fbq('track', 'CompleteRegistration');
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
        source: window.location.href
    };
    
    // Here you would send to your API/Formspree/Google Sheets
    console.log('Quiz data:', data);
    
    // Example with Formspree:
    // fetch('https://formspree.io/f/YOUR_FORM_ID', {
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
