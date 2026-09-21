document.addEventListener('DOMContentLoaded', () => {
    let testData = null;
    let currentPartIndex = 0;
    let answers = {}; // Store user answers: { 1: "answer", 2: "A" }
    let reviewFlags = {}; // Store question review flags: { 1: true }
    let isTestFinished = false;

    // --- URL PARAMETERS & INITIALIZATION ---
    const urlParams = new URLSearchParams(window.location.search);
    const book = urlParams.get('book') || '21';
    const test = urlParams.get('test') || '1';
    const mode = urlParams.get('mode') || 'reading';

    const storageKey = `ielts_answers_c${book}_t${test}_${mode}`;

    // Load saved answers if any
    try {
        const saved = localStorage.getItem(storageKey);
        if (saved) {
            answers = JSON.parse(saved);
        }
    } catch (e) {
        console.warn('Could not load localStorage', e);
    }

    // --- TIMER CONFIGURATION ---
    let timeLeft = 60 * 60; // default 60 min
    if (mode === 'listening') timeLeft = 30 * 60;
    if (mode === 'writing') timeLeft = 60 * 60;
    if (mode === 'full') timeLeft = 150 * 60;

    const timerElement = document.getElementById('timer');
    function updateTimer() {
        if (isTestFinished) return;
        const minutes = Math.floor(timeLeft / 60);
        const seconds = timeLeft % 60;
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        if (timeLeft <= 10 * 60) {
            timerElement.classList.add('warning');
        }
        
        if (timeLeft > 0) {
            timeLeft--;
        } else {
            finishTest(true);
        }
    }
    const timerInterval = setInterval(updateTimer, 1000);

    // --- MODULE SWITCHER ---
    const switchers = {
        'btn-reading': 'view-reading',
        'btn-listening': 'view-listening',
        'btn-writing': 'view-writing'
    };
    const testNames = {
        'btn-reading': 'IELTS Academic Reading',
        'btn-listening': 'IELTS Listening',
        'btn-writing': 'IELTS Academic Writing'
    };

    document.querySelectorAll('.switcher-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            document.querySelectorAll('.switcher-btn').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.view-container').forEach(v => {
                v.classList.remove('active');
                v.style.display = 'none';
            });
            
            e.target.classList.add('active');
            const viewId = switchers[e.target.id];
            const view = document.getElementById(viewId);
            view.style.display = view.classList.contains('split-screen') ? 'flex' : 'block';
            view.classList.add('active');
            document.getElementById('current-test-name').textContent = `Cambridge ${book} Test ${test} - ${testNames[e.target.id]}`;
        });
    });

    // Configure initial view based on mode
    if (mode === 'reading') {
        document.getElementById('btn-listening').style.display = 'none';
        document.getElementById('btn-writing').style.display = 'none';
        document.getElementById('btn-reading').click();
    } else if (mode === 'listening') {
        document.getElementById('btn-reading').style.display = 'none';
        document.getElementById('btn-writing').style.display = 'none';
        document.getElementById('btn-listening').click();
        showSoundCheckModal();
    } else if (mode === 'writing') {
        document.getElementById('btn-reading').style.display = 'none';
        document.getElementById('btn-listening').style.display = 'none';
        document.getElementById('btn-writing').click();
    } else {
        document.getElementById('btn-listening').click();
        showSoundCheckModal();
    }

    // --- FETCH TEST DATA ---
    const currentModule = mode === 'full' ? 'reading' : mode;
    // Try both paths: extracted_data and data/
    const dataSources = [
        `../extracted_data/c${book}_test${test}_${currentModule}.json`,
        `data/c${book}_test${test}.json`,
        `data/c${book}_test${test}_${currentModule}.json`
    ];

    async function loadTestData() {
        for (const path of dataSources) {
            try {
                const res = await fetch(path);
                if (res.ok) {
                    testData = await res.json();
                    initTestEngine();
                    return;
                }
            } catch (err) {}
        }
        // Fallback demo structure if JSON not extracted yet
        console.warn("Could not fetch remote JSON, loading fallback structure.");
        testData = createFallbackData(book, test, currentModule);
        initTestEngine();
    }

    loadTestData();

    // --- INITIALIZE TEST ENGINE ---
    function initTestEngine() {
        if (!testData || !testData.parts || testData.parts.length === 0) {
            document.getElementById('passage-content').innerHTML = '<p style="color:red;">Error: No parts found in test data.</p>';
            return;
        }

        renderPartTabs();
        renderPalette();
        renderPart(0);
        restoreSavedInputs();
    }

    // --- PART TABS NAVIGATION ---
    function renderPartTabs() {
        const tabsContainer = document.getElementById('part-tabs');
        tabsContainer.innerHTML = '';

        testData.parts.forEach((part, index) => {
            const btn = document.createElement('button');
            btn.className = `part-tab-btn ${index === currentPartIndex ? 'active' : ''}`;
            const partLabel = currentModule === 'reading' ? `Passage ${index + 1}` : (currentModule === 'listening' ? `Part ${index + 1}` : `Task ${index + 1}`);
            btn.textContent = partLabel;
            btn.addEventListener('click', () => {
                switchPart(index);
            });
            tabsContainer.appendChild(btn);
        });
    }

    function switchPart(index) {
        currentPartIndex = index;
        document.querySelectorAll('.part-tab-btn').forEach((btn, i) => {
            btn.classList.toggle('active', i === index);
        });
        renderPart(index);
        restoreSavedInputs();
    }

    // --- RENDER CURRENT PART ---
    function renderPart(index) {
        const part = testData.parts[index];
        if (!part) return;

        if (currentModule === 'reading') {
            document.getElementById('passage-content').innerHTML = part.passage || '<p>No passage content available.</p>';
            const questionsContainer = document.getElementById('questions-content');
            questionsContainer.innerHTML = '';
            
            if (part.questions && part.questions.length > 0) {
                part.questions.forEach(q => {
                    const block = document.createElement('div');
                    block.className = 'question-block';
                    block.id = `qblock-${q.id}`;
                    block.innerHTML = `
                        <div class="question-instruction">${q.instruction || ''}</div>
                        <div class="question-body">${q.content || ''}</div>
                    `;
                    questionsContainer.appendChild(block);
                });
            }
        } else if (currentModule === 'listening') {
            const audioElem = document.getElementById('listening-audio');
            if (part.audio_file) {
                let audioSrc = part.audio_file;
                if (!audioSrc.startsWith('http') && !audioSrc.startsWith('/') && !audioSrc.startsWith('../')) {
                    const bookNum = parseInt(book, 10);
                    const bookFolder = bookNum < 10 ? `Cambridge IELTS 0${bookNum}` : `Cambridge IELTS ${bookNum}`;
                    audioSrc = `../${bookFolder}/${audioSrc}`;
                }
                audioElem.src = audioSrc;
                audioElem.onerror = () => {
                    console.warn(`Could not load audio from ${audioSrc}, falling back to default listening audio.`);
                    audioElem.src = 'data/listening.mp3';
                };
            }
            const questionsContainer = document.getElementById('listening-questions-content');
            questionsContainer.innerHTML = '';
            if (part.questions && part.questions.length > 0) {
                part.questions.forEach(q => {
                    const block = document.createElement('div');
                    block.className = 'question-block';
                    block.id = `qblock-${q.id}`;
                    block.innerHTML = `
                        <div class="question-instruction">${q.instruction || ''}</div>
                        <div class="question-body">${q.content || ''}</div>
                    `;
                    questionsContainer.appendChild(block);
                });
            }
        }

        attachInputListeners();
        updateActiveQuestionPalette();
    }

    // --- QUESTION PALETTE (1 - 40) ---
    function renderPalette() {
        const palette = document.getElementById('question-palette');
        palette.innerHTML = '';

        let totalQuestions = 40;
        // Count actual questions if available
        let allQuestions = [];
        testData.parts.forEach(p => {
            if (p.questions) allQuestions.push(...p.questions);
        });
        if (allQuestions.length > 0) {
            totalQuestions = Math.max(40, allQuestions.length);
        }

        for (let i = 1; i <= totalQuestions; i++) {
            const box = document.createElement('div');
            box.className = 'q-box';
            box.id = `qbox-${i}`;
            box.textContent = i;

            if (answers[i]) {
                box.classList.add('answered');
            }
            if (reviewFlags[i]) {
                box.classList.add('review');
            }

            box.addEventListener('click', () => {
                goToQuestion(i);
            });
            palette.appendChild(box);
        }

        // Default highlight box 1
        const firstBox = document.getElementById('qbox-1');
        if (firstBox) firstBox.classList.add('active');
    }

    function goToQuestion(qNum) {
        // Find which part contains question qNum
        let targetPartIndex = -1;
        testData.parts.forEach((p, pIdx) => {
            if (p.questions && p.questions.some(q => q.id === qNum)) {
                targetPartIndex = pIdx;
            }
        });

        if (targetPartIndex !== -1 && targetPartIndex !== currentPartIndex) {
            switchPart(targetPartIndex);
        }

        document.querySelectorAll('.q-box').forEach(b => b.classList.remove('active'));
        const targetBox = document.getElementById(`qbox-${qNum}`);
        if (targetBox) targetBox.classList.add('active');

        // Scroll to question block
        setTimeout(() => {
            const qInput = document.querySelector(`[data-qid="${qNum}"], [name="q${qNum}"]`);
            if (qInput) {
                const block = qInput.closest('.question-block');
                if (block) block.scrollIntoView({ behavior: 'smooth', block: 'center' });
                if (qInput.focus) qInput.focus();
            }
        }, 100);

        // Update review checkbox state
        const reviewCheckbox = document.getElementById('review-checkbox');
        reviewCheckbox.checked = !!reviewFlags[qNum];
    }

    function updateActiveQuestionPalette() {
        const activeBox = document.querySelector('.q-box.active');
        if (activeBox) {
            const qNum = parseInt(activeBox.textContent);
            const reviewCheckbox = document.getElementById('review-checkbox');
            reviewCheckbox.checked = !!reviewFlags[qNum];
        }
    }

    // --- INPUT LISTENERS & STATE PERSISTENCE ---
    function attachInputListeners() {
        // Text Inputs (fill in blank)
        document.querySelectorAll('.ielts-input').forEach(input => {
            input.addEventListener('input', (e) => {
                const qid = e.target.getAttribute('data-qid');
                if (!qid) return;
                const val = e.target.value.trim();
                if (val !== '') {
                    answers[qid] = val;
                } else {
                    delete answers[qid];
                }
                saveAnswers();
                updateBoxState(qid);
            });

            input.addEventListener('focus', (e) => {
                const qid = e.target.getAttribute('data-qid');
                if (qid) highlightBox(qid);
            });
        });

        // Radio Inputs (MCQ / TFNG)
        document.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                const name = e.target.getAttribute('name');
                const qid = name ? name.replace('q', '') : null;
                if (!qid) return;
                if (e.target.checked) {
                    answers[qid] = e.target.value;
                }
                saveAnswers();
                updateBoxState(qid);
            });

            radio.addEventListener('focus', (e) => {
                const name = e.target.getAttribute('name');
                const qid = name ? name.replace('q', '') : null;
                if (qid) highlightBox(qid);
            });
        });
    }

    function updateBoxState(qid) {
        const box = document.getElementById(`qbox-${qid}`);
        if (!box) return;
        if (answers[qid] && answers[qid].trim() !== '') {
            box.classList.add('answered');
        } else {
            box.classList.remove('answered');
        }
    }

    function highlightBox(qid) {
        document.querySelectorAll('.q-box').forEach(b => b.classList.remove('active'));
        const box = document.getElementById(`qbox-${qid}`);
        if (box) box.classList.add('active');
        const reviewCheckbox = document.getElementById('review-checkbox');
        reviewCheckbox.checked = !!reviewFlags[qid];
    }

    function saveAnswers() {
        try {
            localStorage.setItem(storageKey, JSON.stringify(answers));
        } catch (e) {}
    }

    function restoreSavedInputs() {
        Object.keys(answers).forEach(qid => {
            const val = answers[qid];
            // Fill in blanks
            const textInput = document.querySelector(`.ielts-input[data-qid="${qid}"]`);
            if (textInput) textInput.value = val;

            // Radio
            const radio = document.querySelector(`input[name="q${qid}"][value="${val}"]`);
            if (radio) radio.checked = true;

            const box = document.getElementById(`qbox-${qid}`);
            if (box && val.trim() !== '') box.classList.add('answered');
        });
    }

    // --- PREV / NEXT NAVIGATION ---
    document.getElementById('prev-btn').addEventListener('click', () => {
        const activeBox = document.querySelector('.q-box.active');
        if (!activeBox) return;
        const currentQ = parseInt(activeBox.textContent);
        if (currentQ > 1) {
            goToQuestion(currentQ - 1);
        }
    });

    document.getElementById('next-btn').addEventListener('click', () => {
        const activeBox = document.querySelector('.q-box.active');
        if (!activeBox) return;
        const currentQ = parseInt(activeBox.textContent);
        if (currentQ < 40) {
            goToQuestion(currentQ + 1);
        }
    });

    // --- REVIEW CHECKBOX ---
    const reviewCheckbox = document.getElementById('review-checkbox');
    reviewCheckbox.addEventListener('change', (e) => {
        const activeBox = document.querySelector('.q-box.active');
        if (!activeBox) return;
        const qNum = parseInt(activeBox.textContent);
        if (e.target.checked) {
            reviewFlags[qNum] = true;
            activeBox.classList.add('review');
        } else {
            delete reviewFlags[qNum];
            activeBox.classList.remove('review');
        }
    });

    // --- WRITING WORD COUNTER ---
    const editor = document.getElementById('writing-editor');
    const wordCountDisplay = document.getElementById('word-count');
    if (editor) {
        editor.addEventListener('input', () => {
            const text = editor.value.trim();
            const words = text ? text.split(/\s+/).length : 0;
            wordCountDisplay.textContent = words;
        });
    }

    // --- SOUND CHECK MODAL ---
    function showSoundCheckModal() {
        const modal = document.getElementById('sound-check-modal');
        if (modal) modal.style.display = 'flex';
    }

    const testSoundBtn = document.getElementById('test-sound-btn');
    if (testSoundBtn) {
        testSoundBtn.addEventListener('click', () => {
            // Web Audio API beep sound test
            try {
                const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(440, audioCtx.currentTime); // A4 note
                gain.gain.setValueAtTime(0.1, audioCtx.currentTime);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.5);
                testSoundBtn.textContent = '🔊 Sound Playing... OK!';
                setTimeout(() => { testSoundBtn.textContent = '🔊 Play Sample Sound'; }, 1000);
            } catch (e) {
                alert("Audio test completed.");
            }
        });
    }

    const startListeningBtn = document.getElementById('start-listening-btn');
    if (startListeningBtn) {
        startListeningBtn.addEventListener('click', () => {
            document.getElementById('sound-check-modal').style.display = 'none';
            const audio = document.getElementById('listening-audio');
            if (audio) audio.play().catch(() => {});
        });
    }

    // --- SPLIT RESIZERS ---
    setupResizer('resizer', '#view-reading .left-pane', '#view-reading .right-pane', '#view-reading');
    setupResizer('resizer-writing', '#view-writing .left-pane', '#view-writing .right-pane', '#view-writing');

    function setupResizer(resizerId, leftPaneSelector, rightPaneSelector, containerSelector) {
        const resizer = document.getElementById(resizerId);
        const leftPane = document.querySelector(leftPaneSelector);
        const rightPane = document.querySelector(rightPaneSelector);
        const container = document.querySelector(containerSelector);
        if (!resizer || !leftPane || !rightPane || !container) return;

        let isResizing = false;
        resizer.addEventListener('mousedown', () => {
            isResizing = true;
            document.body.style.cursor = 'col-resize';
        });

        document.addEventListener('mousemove', (e) => {
            if (!isResizing) return;
            const containerWidth = container.offsetWidth;
            let leftWidth = (e.clientX / containerWidth) * 100;
            if (leftWidth < 20) leftWidth = 20;
            if (leftWidth > 80) leftWidth = 80;
            leftPane.style.flex = `0 0 ${leftWidth}%`;
            rightPane.style.flex = `1 1 auto`;
        });

        document.addEventListener('mouseup', () => {
            isResizing = false;
            document.body.style.cursor = 'default';
        });
    }

    // --- HIGHLIGHT AND NOTES CONTEXT MENU ---
    const passageContainer = document.getElementById('passage-content');
    const contextMenu = document.getElementById('context-menu');
    let currentSelectionRange = null;

    if (passageContainer && contextMenu) {
        passageContainer.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            const selection = window.getSelection();
            if (selection.toString().trim() !== '') {
                currentSelectionRange = selection.getRangeAt(0);
                contextMenu.style.display = 'block';
                contextMenu.style.left = `${e.pageX}px`;
                contextMenu.style.top = `${e.pageY}px`;
            }
        });

        document.addEventListener('click', (e) => {
            if (!contextMenu.contains(e.target)) {
                contextMenu.style.display = 'none';
            }
        });

        document.getElementById('menu-highlight').addEventListener('click', () => {
            if (currentSelectionRange) {
                const span = document.createElement('span');
                span.className = 'highlighted-text';
                currentSelectionRange.surroundContents(span);
                window.getSelection().removeAllRanges();
                contextMenu.style.display = 'none';
            }
        });

        document.getElementById('menu-notes').addEventListener('click', () => {
            if (currentSelectionRange) {
                const note = prompt("Enter your note:");
                if (note) {
                    const span = document.createElement('span');
                    span.className = 'highlighted-text';
                    currentSelectionRange.surroundContents(span);
                    
                    const noteIndicator = document.createElement('span');
                    noteIndicator.className = 'note-indicator';
                    noteIndicator.textContent = '📝';
                    noteIndicator.title = note;
                    noteIndicator.addEventListener('click', () => alert("Note: " + note));
                    span.appendChild(noteIndicator);
                    
                    window.getSelection().removeAllRanges();
                }
                contextMenu.style.display = 'none';
            }
        });

        document.getElementById('menu-clear').addEventListener('click', () => {
            contextMenu.style.display = 'none';
        });
    }

    // --- SETTINGS MODAL ---
    const settingsBtn = document.querySelector('.controls .control-btn[title="Settings"]');
    const settingsModal = document.getElementById('settings-modal');
    const closeSettingsBtn = document.getElementById('close-settings-btn');
    if (settingsBtn && settingsModal) {
        settingsBtn.addEventListener('click', () => { settingsModal.style.display = 'flex'; });
        closeSettingsBtn.addEventListener('click', () => { settingsModal.style.display = 'none'; });
    }

    document.getElementById('text-size-select').addEventListener('change', (e) => {
        document.body.classList.remove('text-large', 'text-xlarge');
        if (e.target.value === 'large') document.body.classList.add('text-large');
        if (e.target.value === 'xlarge') document.body.classList.add('text-xlarge');
    });

    document.getElementById('color-scheme-select').addEventListener('change', (e) => {
        document.body.classList.remove('theme-yellow-on-black', 'theme-blue-on-white');
        if (e.target.value === 'yellow-on-black') document.body.classList.add('theme-yellow-on-black');
        if (e.target.value === 'blue-on-white') document.body.classList.add('theme-blue-on-white');
    });

    // --- FINISH TEST & AUTOMATIC SCORING SYSTEM ---
    const finishBtn = document.querySelector('.finish-btn');
    finishBtn.addEventListener('click', () => {
        if (confirm("Are you sure you want to finish the test? Your answers will be submitted and evaluated.")) {
            finishTest(false);
        }
    });

    function finishTest(isTimeUp = false) {
        isTestFinished = true;
        clearInterval(timerInterval);

        // Calculate score
        let totalQuestions = 0;
        let correctCount = 0;
        let wrongCount = 0;
        let unansweredCount = 0;

        let questionResults = []; // [{ id, userAns, correctAns, isCorrect, isUnanswered }]

        // Extract questions and compare
        testData.parts.forEach(part => {
            if (part.questions) {
                part.questions.forEach(q => {
                    totalQuestions++;
                    const userAns = answers[q.id] ? answers[q.id].trim() : '';
                    const correctAns = q.answer ? q.answer.toString().trim() : '';

                    let isCorrect = false;
                    let isUnanswered = false;

                    if (!userAns) {
                        isUnanswered = true;
                        unansweredCount++;
                    } else if (checkAnswerMatch(userAns, correctAns)) {
                        isCorrect = true;
                        correctCount++;
                    } else {
                        wrongCount++;
                    }

                    questionResults.push({
                        id: q.id,
                        userAns: userAns || '(No Answer)',
                        correctAns: correctAns || 'N/A',
                        isCorrect,
                        isUnanswered
                    });
                });
            }
        });

        // If no questions in JSON, fallback to 40
        if (totalQuestions === 0) totalQuestions = 40;

        // Band Calculation
        const bandScore = calculateBandScore(correctCount, currentModule);
        const accuracy = totalQuestions > 0 ? Math.round((correctCount / totalQuestions) * 100) : 0;

        // Render Results Modal
        document.getElementById('result-band-score').textContent = bandScore;
        document.getElementById('result-raw-score').textContent = `${correctCount} / ${totalQuestions}`;
        document.getElementById('result-accuracy').textContent = `${accuracy}%`;
        document.getElementById('res-correct-count').textContent = correctCount;
        document.getElementById('res-wrong-count').textContent = wrongCount;
        document.getElementById('res-unanswered-count').textContent = unansweredCount;

        document.getElementById('total-q-count').textContent = totalQuestions;
        document.getElementById('incorrect-q-count').textContent = wrongCount + unansweredCount;
        document.getElementById('correct-q-count').textContent = correctCount;

        renderResultsTable(questionResults, 'all');

        // Show Modal
        document.getElementById('results-modal').style.display = 'flex';

        // Review Button
        document.getElementById('review-test-btn').onclick = () => {
            document.getElementById('results-modal').style.display = 'none';
            enableReviewMode(questionResults);
        };

        document.getElementById('close-results-x').onclick = () => {
            document.getElementById('results-modal').style.display = 'none';
        };

        // Filter Buttons
        document.querySelectorAll('.filter-btn').forEach(fBtn => {
            fBtn.addEventListener('click', (e) => {
                document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                renderResultsTable(questionResults, e.target.getAttribute('data-filter'));
            });
        });
    }

    function checkAnswerMatch(userVal, correctVal) {
        if (!userVal || !correctVal) return false;
        const normUser = userVal.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").trim();
        const normCorrect = correctVal.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").trim();

        // Exact match
        if (normUser === normCorrect) return true;

        // Alternative answers: e.g. "autumn / fall" or "autumn or fall"
        const alts = correctVal.split(/\/|\bor\b/i).map(a => a.toLowerCase().replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g, "").trim());
        return alts.includes(normUser);
    }

    function calculateBandScore(rawScore, moduleType) {
        // Academic Reading Band Scale (Standard Cambridge)
        if (moduleType === 'reading') {
            if (rawScore >= 39) return '9.0';
            if (rawScore >= 37) return '8.5';
            if (rawScore >= 35) return '8.0';
            if (rawScore >= 33) return '7.5';
            if (rawScore >= 30) return '7.0';
            if (rawScore >= 27) return '6.5';
            if (rawScore >= 23) return '6.0';
            if (rawScore >= 19) return '5.5';
            if (rawScore >= 15) return '5.0';
            if (rawScore >= 13) return '4.5';
            if (rawScore >= 10) return '4.0';
            if (rawScore >= 8) return '3.5';
            if (rawScore >= 6) return '3.0';
            return '2.5';
        }
        // Listening Band Scale (Standard Cambridge)
        if (moduleType === 'listening') {
            if (rawScore >= 39) return '9.0';
            if (rawScore >= 37) return '8.5';
            if (rawScore >= 35) return '8.0';
            if (rawScore >= 32) return '7.5';
            if (rawScore >= 30) return '7.0';
            if (rawScore >= 26) return '6.5';
            if (rawScore >= 23) return '6.0';
            if (rawScore >= 18) return '5.5';
            if (rawScore >= 16) return '5.0';
            if (rawScore >= 13) return '4.5';
            if (rawScore >= 10) return '4.0';
            return '3.5';
        }
        return 'N/A';
    }

    function renderResultsTable(results, filter) {
        const tbody = document.getElementById('result-table-body');
        tbody.innerHTML = '';

        const filtered = results.filter(r => {
            if (filter === 'correct') return r.isCorrect;
            if (filter === 'incorrect') return !r.isCorrect;
            return true;
        });

        if (filtered.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" style="text-align:center; color:#888;">No questions match this filter.</td></tr>';
            return;
        }

        filtered.forEach(r => {
            const row = document.createElement('tr');
            let statusHtml = '';
            if (r.isCorrect) {
                statusHtml = '<span class="status-badge correct">✅ Correct</span>';
            } else if (r.isUnanswered) {
                statusHtml = '<span class="status-badge unanswered">⚠️ Unanswered</span>';
            } else {
                statusHtml = '<span class="status-badge wrong">❌ Incorrect</span>';
            }

            row.innerHTML = `
                <td><strong>Q${r.id}</strong></td>
                <td><span style="font-family:monospace; color:${r.isCorrect ? '#155724' : '#721c24'}">${escapeHtml(r.userAns)}</span></td>
                <td><strong style="color: #0056b3;">${escapeHtml(r.correctAns)}</strong></td>
                <td>${statusHtml}</td>
            `;
            tbody.appendChild(row);
        });
    }

    function enableReviewMode(results) {
        document.body.classList.add('review-mode');

        results.forEach(r => {
            const box = document.getElementById(`qbox-${r.id}`);
            if (box) {
                box.classList.remove('answered', 'active');
                if (r.isCorrect) {
                    box.classList.add('res-correct');
                } else {
                    box.classList.add('res-wrong');
                }
            }

            // Tag inputs
            const textInput = document.querySelector(`.ielts-input[data-qid="${r.id}"]`);
            if (textInput) {
                textInput.readOnly = true;
                textInput.classList.add(r.isCorrect ? 'is-correct' : 'is-wrong');
                if (!r.isCorrect && !textInput.nextElementSibling?.classList?.contains('correct-ans-tag')) {
                    const tag = document.createElement('span');
                    tag.className = 'correct-ans-tag';
                    tag.textContent = `Ans: ${r.correctAns}`;
                    textInput.after(tag);
                }
            }
        });
    }

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
    }

    function createFallbackData(bookNum, testNum, mod) {
        return {
            book: parseInt(bookNum),
            test: parseInt(testNum),
            module: mod,
            title: `Cambridge ${bookNum} Test ${testNum}`,
            parts: [
                {
                    part_number: 1,
                    title: "Part 1 / Passage 1",
                    passage: "<h3>Sample Test Passage</h3><p>The extraction for this test is currently in progress via GitHub Actions. Once the process finishes, the real questions and passages from Cambridge " + bookNum + " will be dynamically loaded.</p>",
                    questions: [
                        { id: 1, type: "fill_in_the_blank", instruction: "Complete the notes below. Choose ONE WORD ONLY.", content: "<p>The capital of France is <b>1</b> <input type='text' data-qid='1' class='ielts-input' /></p>", answer: "Paris" },
                        { id: 2, type: "multiple_choice", instruction: "Choose the correct letter A, B, C or D.", content: "<p><b>2</b> What is the best score in IELTS?</p><label><input type='radio' name='q2' value='A'> A. Band 7</label><br><label><input type='radio' name='q2' value='B'> B. Band 9</label><br><label><input type='radio' name='q2' value='C'> C. Band 10</label>", answer: "B" }
                    ]
                }
            ]
        };
    }
});
