document.addEventListener('DOMContentLoaded', () => {
    // 1. Tab Switching Logic
    const tabBtns = document.querySelectorAll('.tab-btn');
    const featureCards = document.querySelectorAll('.feature-card');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            
            tabBtns.forEach(b => b.classList.remove('active'));
            featureCards.forEach(card => card.classList.remove('active-card'));

            btn.classList.add('active');
            const targetCard = document.getElementById(targetId);
            if (targetCard) {
                targetCard.classList.add('active-card');
            }
        });
    });

    // Helper: Show Loading Spinner in output box
    function showLoading(outputEl, message = 'EduGenie is thinking...') {
        outputEl.classList.remove('hidden');
        outputEl.innerHTML = `
            <div class="loading-state">
                <div class="spinner"></div>
                <span>${message}</span>
            </div>
        `;
    }

    // Helper: Render markdown if marked is loaded, otherwise plain text
    function renderMarkdown(text) {
        if (window.marked && typeof window.marked.parse === 'function') {
            return window.marked.parse(text);
        }
        return text.replace(/\n/g, '<br>');
    }

    // 2. Q&A Form Handler
    const qaForm = document.getElementById('qaForm');
    const qaResult = document.getElementById('qaResult');

    qaForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = document.getElementById('question').value.trim();
        if (!question) return;

        showLoading(qaResult, 'Finding the best answer...');

        try {
            const response = await fetch(`/qa?question=${encodeURIComponent(question)}`);
            const data = await response.json();

            if (data.answer) {
                qaResult.innerHTML = `
                    <div class="output-title"><i class="fa-solid fa-comment-dots"></i> Answer:</div>
                    <div class="output-content">${renderMarkdown(data.answer)}</div>
                `;
            } else if (data.error) {
                qaResult.innerHTML = `<div class="output-content" style="color: #f87171;">❌ ${data.error}</div>`;
            }
        } catch (err) {
            qaResult.innerHTML = `<div class="output-content" style="color: #f87171;">⚠️ Network Error: Unable to fetch answer from backend.</div>`;
        }
    });

    // 3. Explanation Form Handler
    const explainForm = document.getElementById('explainForm');
    const explainResult = document.getElementById('explainResult');

    explainForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const topic = document.getElementById('topic').value.trim();
        if (!topic) return;

        showLoading(explainResult, 'Generating concept explanation...');

        try {
            const response = await fetch('/explain', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ topic: topic })
            });
            const data = await response.json();

            if (data.explanation) {
                explainResult.innerHTML = `
                    <div class="output-title"><i class="fa-solid fa-book-open"></i> Explanation for "${data.topic || topic}":</div>
                    <div class="output-content">${renderMarkdown(data.explanation)}</div>
                `;
            } else if (data.error) {
                explainResult.innerHTML = `<div class="output-content" style="color: #f87171;">❌ ${data.error}</div>`;
            }
        } catch (err) {
            explainResult.innerHTML = `<div class="output-content" style="color: #f87171;">⚠️ Network Error: Unable to fetch explanation.</div>`;
        }
    });

    // 4. Summarize Form Handler
    const summaryForm = document.getElementById('summaryForm');
    const summaryResult = document.getElementById('summaryResult');

    summaryForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = document.getElementById('summaryText').value.trim();
        if (!text) return;

        showLoading(summaryResult, 'Summarizing passage...');

        try {
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            const data = await response.json();

            if (data.summary) {
                summaryResult.innerHTML = `
                    <div class="output-title"><i class="fa-solid fa-compress-alt"></i> Summary:</div>
                    <div class="output-content">${renderMarkdown(data.summary)}</div>
                `;
            } else if (data.error) {
                summaryResult.innerHTML = `<div class="output-content" style="color: #f87171;">❌ ${data.error}</div>`;
            }
        } catch (err) {
            summaryResult.innerHTML = `<div class="output-content" style="color: #f87171;">⚠️ Network Error: Unable to fetch summary.</div>`;
        }
    });

    // 5. Quiz Form Handler & Interactive Renderer
    const quizForm = document.getElementById('quizForm');
    const quizResult = document.getElementById('quizResult');

    quizForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const text = document.getElementById('quizText').value.trim();
        if (!text) return;

        showLoading(quizResult, 'Crafting multiple-choice quiz questions...');

        try {
            const response = await fetch('/quiz', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });
            const data = await response.json();

            if (data.quiz && Array.isArray(data.quiz)) {
                renderQuiz(data.quiz);
            } else if (data.error) {
                quizResult.innerHTML = `<div class="output-content" style="color: #f87171;">❌ ${data.error}</div>`;
            }
        } catch (err) {
            quizResult.innerHTML = `<div class="output-content" style="color: #f87171;">⚠️ Network Error: Unable to generate quiz.</div>`;
        }
    });

    function renderQuiz(quizItems) {
        if (!quizItems || quizItems.length === 0) {
            quizResult.innerHTML = `<div class="output-content">No quiz questions were generated. Please try again.</div>`;
            return;
        }

        let html = `
            <div class="quiz-container">
                <div class="output-title"><i class="fa-solid fa-list-check"></i> Generated Quiz (${quizItems.length} Questions):</div>
        `;

        quizItems.forEach((q, index) => {
            const qNum = index + 1;
            const optionsHtml = q.options.map((opt, optIndex) => `
                <label class="quiz-option-label" for="q${qNum}_opt${optIndex}">
                    <input type="radio" id="q${qNum}_opt${optIndex}" name="question_${qNum}" value="${escapeHtml(opt)}">
                    <span>${escapeHtml(opt)}</span>
                </label>
            `).join('');

            html += `
                <div class="quiz-card" data-question-index="${index}" data-correct-answer="${escapeHtml(q.answer)}">
                    <div class="quiz-question">Q${qNum}: ${escapeHtml(q.question)}</div>
                    <div class="quiz-options">
                        ${optionsHtml}
                    </div>
                    <button class="check-answer-btn" onclick="checkQuizAnswer(this)">Check Answer</button>
                    <div class="quiz-feedback-container"></div>
                </div>
            `;
        });

        html += `</div>`;
        quizResult.classList.remove('hidden');
        quizResult.innerHTML = html;
    }

    // Global helper to check individual question answer matching screenshot logic on page 14
    window.checkQuizAnswer = function(buttonEl) {
        const card = buttonEl.closest('.quiz-card');
        const correctAnswer = card.getAttribute('data-correct-answer');
        const selectedRadio = card.querySelector('input[type="radio"]:checked');
        const feedbackContainer = card.querySelector('.quiz-feedback-container');

        if (!selectedRadio) {
            feedbackContainer.innerHTML = `<div class="quiz-feedback incorrect">⚠️ Please select an option first!</div>`;
            return;
        }

        const selectedValue = selectedRadio.value;
        if (selectedValue === correctAnswer) {
            feedbackContainer.innerHTML = `<div class="quiz-feedback correct">✅ Correct!</div>`;
        } else {
            feedbackContainer.innerHTML = `<div class="quiz-feedback incorrect">❌ Incorrect. Correct answer: ${escapeHtml(correctAnswer)}</div>`;
        }
    };

    function escapeHtml(str) {
        return (str || '').toString()
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // 6. Learning Path Form Handler
    const learnForm = document.getElementById('learnForm');
    const learnResult = document.getElementById('learnResult');

    learnForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const topic = document.getElementById('learnTopic').value.trim();
        if (!topic) return;

        showLoading(learnResult, 'Designing personalized learning roadmap...');

        try {
            const response = await fetch(`/learn/recommendations?topic=${encodeURIComponent(topic)}`);
            const data = await response.json();

            if (data.recommendation) {
                learnResult.innerHTML = `
                    <div class="output-title"><i class="fa-solid fa-route"></i> Learning Recommendations for "${data.topic || topic}":</div>
                    <div class="output-content">${renderMarkdown(data.recommendation)}</div>
                `;
            } else if (data.error) {
                learnResult.innerHTML = `<div class="output-content" style="color: #f87171;">❌ ${data.error}</div>`;
            }
        } catch (err) {
            learnResult.innerHTML = `<div class="output-content" style="color: #f87171;">⚠️ Network Error: Unable to fetch learning path.</div>`;
        }
    });
});
