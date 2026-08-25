export const themes = [
  { id: 'love', label: '关系与靠近', hint: '关于一段关系，或你与自己的距离' },
  { id: 'work', label: '工作与选择', hint: '关于正在犹豫的方向和下一步' },
  { id: 'mood', label: '此刻心情', hint: '把注意力放回今天的自己' },
  { id: 'future', label: '未来方向', hint: '看看什么正在慢慢成形' },
  { id: 'open', label: '随便问问', hint: '不设问题，让牌先说一句话' }
];

export const moods = ['犹豫', '期待', '疲惫', '失落', '好奇'];

export const followUps = [
  '我真正担心的是什么？',
  '我现在可以做什么？',
  '我忽略了什么？'
];

export const cards = [
  { id: 'fool', name: '愚者', number: '0', symbol: '0', keywords: '起点 · 信任 · 自由', upright: '新的旅程正在向你打开。你不必先知道所有答案，先允许自己迈出第一步。', reversed: '你可能把谨慎误认为胆怯，也可能把冲动误认为自由。出发前，确认脚下还有一小块稳固的地方。', themes: { love: '关系里有新鲜空气。放下预设，真诚地表达一次好奇。', work: '新的尝试值得被认真对待，不必等到完全准备好才开始。', mood: '今天可以只负责走一步，不用把整条路都想明白。', future: '未来不是一张写好的地图，而是你走出去后才显现的路。', open: '有一扇门没有上锁。你想不想试着推开它？' }, actions: ['把想做的事拆成一个十分钟能完成的小动作。', '给一个新想法留下试验的空间，不急着评判它。'] },
  { id: 'magician', name: '魔术师', number: 'I', symbol: 'I', keywords: '行动 · 资源 · 创造', upright: '你手边已经有比想象中更多的资源。真正缺少的，也许只是把它们放在一起。', reversed: '能量有些分散，或许你在等待一个更完美的工具。先把已有的东西用起来。', themes: { love: '你拥有改变相处方式的主动权，一句清楚的话比猜测更有力量。', work: '把能力、经验和机会连接起来，今天适合开始搭建。', mood: '别只观察自己的情绪，也可以温柔地为它做一点安排。', future: '你不是被动等待未来的人，你正在参与它的形成。', open: '你手里的那张牌，可能比你以为的更有用。' }, actions: ['列出手边的三个资源，并选择一个立刻使用。', '把一个模糊愿望写成可以执行的句子。'] },
  { id: 'high-priestess', name: '女祭司', number: 'II', symbol: 'II', keywords: '直觉 · 静默 · 内在知识', upright: '答案暂时藏在安静处。你已经察觉到某种感觉，先不要急着用别人的声音覆盖它。', reversed: '你可能已经听见了内心，却不断要求外界替你确认。留意那些被你略过的小信号。', themes: { love: '关系中有未说出口的部分，先听见自己真正想要什么。', work: '暂缓表态，收集更多信息。沉默不等于停滞。', mood: '今天需要一点不被打扰的时间，让情绪自己浮上来。', future: '不是所有未来都要立刻揭晓，有些答案需要等待成熟。', open: '你心里其实有一个很轻的回答，只是它说话很小声。' }, actions: ['给自己留出十分钟安静时间，不输入任何新信息。', '写下第一个直觉，再写下你为什么不相信它。'] },
  { id: 'empress', name: '皇后', number: 'III', symbol: 'III', keywords: '滋养 · 丰盛 · 感受', upright: '你正在进入适合生长的阶段。照顾身体、关系和感受，本身就是重要的推进。', reversed: '给予太多可能让你忘了自己也需要被照顾。丰盛不该以消耗自己为代价。', themes: { love: '亲近感需要被照料，小小的关心会比宏大的承诺更有重量。', work: '让好的想法长出来，给它时间、空间和持续的关注。', mood: '先照顾最基础的需要：吃饭、休息、呼吸和一点阳光。', future: '你正在播种，结果需要时间，不必每天把土挖开确认。', open: '今天适合对自己好一点，柔软并不是退让。' }, actions: ['完成一件能让身体舒服一点的小事。', '给正在成长的计划留出固定的照料时间。'] },
  { id: 'emperor', name: '皇帝', number: 'IV', symbol: 'IV', keywords: '边界 · 结构 · 稳定', upright: '清晰的边界会带来自由。现在适合把混乱的事情整理成几个可以掌控的部分。', reversed: '控制感可能变得过重。真正稳定的结构，也应该允许变化和呼吸。', themes: { love: '坦白说出边界，关系反而会更安全。', work: '适合建立规则、优先级和可执行的计划。', mood: '当情绪太散时，先恢复一点日常秩序。', future: '未来需要一个稳固支点，但不需要把所有可能性锁死。', open: '你可以为自己设一道温柔而清楚的界线。' }, actions: ['只选三个今天必须完成的事项。', '明确说出一次你的时间、精力或情绪边界。'] },
  { id: 'hierophant', name: '教皇', number: 'V', symbol: 'V', keywords: '传统 · 学习 · 指引', upright: '经验和可靠的指导可以成为桥梁。你不必独自摸索，也可以从成熟的方法中借一点力。', reversed: '别人的规则不一定适合你的处境。尊重传统，也保留重新提问的权利。', themes: { love: '共同的价值观比一时的热烈更能支撑关系。', work: '向值得信任的人请教，会比反复独自试错更快。', mood: '找一个安全的人或稳定的习惯，让自己重新落地。', future: '学习和积累会在未来某个时刻显出重量。', open: '有些答案不在更远的地方，而在被验证过的方法里。' }, actions: ['向一个你信任的人提出一个具体问题。', '找一个成熟范例，看看它如何处理相似处境。'] },
  { id: 'lovers', name: '恋人', number: 'VI', symbol: 'VI', keywords: '选择 · 联结 · 价值', upright: '真正的选择不是选哪个更完美，而是确认什么与你的价值一致。', reversed: '你可能在迎合期待，或把不选择也当成了一种选择。诚实会带来方向。', themes: { love: '靠近需要真实，而不是表演成对方期待的样子。', work: '选择一条能与你长期价值观相处的路。', mood: '问问自己：我现在最需要的，是安慰、空间还是行动？', future: '未来的分岔口正在形成，选择会让你更清楚自己是谁。', open: '你正在选择的不只是事情，还有你想成为的人。' }, actions: ['写下两个选择各自需要你付出的代价。', '把一次真实的感受说得简单而直接。'] },
  { id: 'chariot', name: '战车', number: 'VII', symbol: 'VII', keywords: '意志 · 前进 · 方向', upright: '力量来自方向一致。把分散的情绪和目标收拢起来，你比想象中更能向前。', reversed: '用力过猛会让你偏离方向。暂停校准，不是放弃。', themes: { love: '关系需要共同的方向，而不是一方不断拉着另一方前进。', work: '今天适合推进一个明确目标，先不要同时征服所有事情。', mood: '给情绪一个出口，再决定下一步往哪里走。', future: '道路会在行动中变清晰，不必等所有阻力消失。', open: '缰绳在你手里，方向比速度更重要。' }, actions: ['为最重要的目标安排一个不被打断的时间段。', '删掉一个正在分散你注意力的任务。'] },
  { id: 'strength', name: '力量', number: 'VIII', symbol: 'VIII', keywords: '勇气 · 温柔 · 驯服', upright: '真正的力量不需要提高音量。你可以带着害怕，依然温柔而坚定地行动。', reversed: '你可能对自己太苛刻，或把压抑误认为坚强。先放松握紧的手。', themes: { love: '耐心和坦诚会比争胜更能拉近彼此。', work: '持续而稳定的努力，比短暂爆发更能改变局面。', mood: '不用消灭情绪，试着和它一起坐一会儿。', future: '你正在培养一种不会轻易被外界带走的内在力量。', open: '柔软不是弱点，它是你与世界相处的另一种勇气。' }, actions: ['把自我批评改写成一句具体、友善的提醒。', '做一件需要耐心而不是速度的事。'] },
  { id: 'hermit', name: '隐者', number: 'IX', symbol: 'IX', keywords: '独处 · 寻找 · 真理', upright: '暂时离开喧闹，答案会更容易被听见。独处不是退场，而是重新校准。', reversed: '独处正在变成隔绝吗？你也许需要一个可靠的连接，而不是更多的封闭。', themes: { love: '先理解自己的需要，再决定如何与别人靠近。', work: '退一步整理方法，独立思考会带来真正的进展。', mood: '给自己安静，但不要把所有人都关在门外。', future: '下一步不需要掌声，它需要与你内心一致。', open: '你正在寻找的光，可能来自自己手里的一盏小灯。' }, actions: ['安排一段不被打扰的独处时间。', '把最近反复出现的一个问题写下来，不急着回答。'] },
  { id: 'wheel', name: '命运之轮', number: 'X', symbol: 'X', keywords: '变化 · 周期 · 转机', upright: '局面正在转动。你无法控制所有变量，但可以决定自己如何迎接变化。', reversed: '某个旧循环还没有结束。别急着把暂时的停滞解释成失败。', themes: { love: '关系可能进入新阶段，顺势观察比强行定义更重要。', work: '新的机会正在靠近，保持准备，也保持弹性。', mood: '情绪会变化，今天的感受不是永久结论。', future: '转机常常以意料之外的方式出现，给偶然留一点位置。', open: '轮子已经开始转动，故事还没有写完。' }, actions: ['为计划准备一个可调整的备选方案。', '注意今天出现的一次意外连接或机会。'] },
  { id: 'justice', name: '正义', number: 'XI', symbol: 'XI', keywords: '诚实 · 平衡 · 结果', upright: '看清事实，承认自己的部分，然后做出与价值一致的决定。', reversed: '你可能在逃避某个事实，或对自己使用了不公平的标准。', themes: { love: '关系需要对等与诚实，不要只计算谁付出更多。', work: '把事实、责任和结果分开看，决定会更清楚。', mood: '允许自己感受，但也温柔地辨认事实与想象。', future: '接下来的结果会回应今天的选择，诚实是最稳的方向。', open: '答案不一定顺耳，但它会让你重新站稳。' }, actions: ['把事实、猜测和担心分别写在三列。', '做一个对未来的自己也公平的选择。'] },
  { id: 'hanged-man', name: '倒吊人', number: 'XII', symbol: 'XII', keywords: '暂停 · 换位 · 放下', upright: '暂时不动也是一种行动。换一个角度，你会看见原本被惯性遮住的东西。', reversed: '等待可能已经变成拖延。问问自己，你是在观察，还是害怕承担选择。', themes: { love: '放下想立刻得到答案的执着，先看看关系真正需要什么。', work: '换一个方法或顺序，暂停并不代表失去进度。', mood: '允许自己今天不解决全部问题，恢复视角本身就很重要。', future: '有些门必须等你改变看法后才会打开。', open: '你不一定需要更多力气，也许需要换一个方向看。' }, actions: ['暂缓一个冲动决定，给它一个晚上。', '从对立面的角度重新描述当前问题。'] }
];

export function createSeededRandom(seed = Date.now()) {
  let value = Math.abs(Number(seed)) || 1;
  return () => {
    value = (value * 1664525 + 1013904223) % 4294967296;
    return value / 4294967296;
  };
}

export function drawCard(deck, random = Math.random, excludedIds = []) {
  const available = deck.filter(card => !excludedIds.includes(card.id));
  const card = available[Math.floor(random() * available.length)];
  const orientation = random() > 0.72 ? '逆位' : '正位';
  return { card, orientation };
}

export function buildReading(card, themeId, mood, followUp, orientation) {
  const themeText = card.themes[themeId] || card.themes.open;
  const baseText = orientation === '逆位' ? card.reversed : card.upright;
  const followText = followUp.includes('担心')
    ? `你可以留意“${mood}”背后真正想被保护的部分。`
    : followUp.includes('做什么')
      ? '答案不要求你立刻完成一切，只邀请你先做一件真实而具体的小事。'
      : '不要只看眼前的表面，给那些被忽略的感受留一点位置。';
  const actions = card.actions;
  return {
    title: `${card.name} · ${orientation}`,
    body: `${baseText} ${themeText} ${followText}`,
    action: actions[Math.floor((mood.length + followUp.length) % actions.length)],
    keywords: card.keywords
  };
}

const state = { theme: 'open', mood: '好奇', drawn: null, history: loadHistory() };

function loadHistory() {
  try { return JSON.parse(localStorage.getItem('today-heart-history') || '[]'); } catch { return []; }
}

function saveHistory(item) {
  state.history = [item, ...state.history].slice(0, 8);
  localStorage.setItem('today-heart-history', JSON.stringify(state.history));
}

function $(selector) { return document.querySelector(selector); }

function renderThemeOptions() {
  $('#theme-options').innerHTML = themes.map(theme => `<button class="choice ${theme.id === state.theme ? 'selected' : ''}" data-theme="${theme.id}"><strong>${theme.label}</strong><span>${theme.hint}</span></button>`).join('');
  $('#mood-options').innerHTML = moods.map(mood => `<button class="mood ${mood === state.mood ? 'selected' : ''}" data-mood="${mood}">${mood}</button>`).join('');
}

function renderHistory() {
  const history = $('#history');
  history.innerHTML = state.history.length ? state.history.map(item => `<li><span>${item.card}</span><small>${item.orientation} · ${item.theme}</small></li>`).join('') : '<li class="empty">还没有留下牌迹</li>';
}

function setPhase(phase) {
  document.body.dataset.phase = phase;
  document.querySelectorAll('[data-phase]').forEach(el => el.hidden = el.dataset.phase !== phase);
}

function draw() {
  state.drawn = drawCard(cards, Math.random, state.history.map(item => item.id));
  const { card, orientation } = state.drawn;
  $('.card-face .card-number').textContent = card.number;
  $('.card-face .card-name').textContent = card.name;
  $('.card-face .card-symbol').textContent = card.symbol;
  $('.card-face .card-keywords').textContent = card.keywords;
  $('.card').classList.remove('flipped');
  $('#draw-button').disabled = true;
  setPhase('reveal');
  setTimeout(() => $('.card').classList.add('flipped'), 500);
  setTimeout(() => { $('#card-status').textContent = `${card.name} · ${orientation}`; $('#followup-options').innerHTML = followUps.map(text => `<button class="followup" data-followup="${text}">${text}<span>↗</span></button>`).join(''); }, 900);
}

function showReading(followUp) {
  const { card, orientation } = state.drawn;
  const theme = themes.find(item => item.id === state.theme);
  const reading = buildReading(card, state.theme, state.mood, followUp, orientation);
  $('#reading-title').textContent = reading.title;
  $('#reading-keywords').textContent = reading.keywords;
  $('#reading-body').textContent = reading.body;
  $('#reading-action').textContent = reading.action;
  $('#reading-theme').textContent = `${theme.label} · ${state.mood}`;
  saveHistory({ id: card.id, card: card.name, orientation, theme: theme.label, date: new Date().toISOString() });
  renderHistory();
  setPhase('reading');
}

function reset() { state.drawn = null; renderThemeOptions(); setPhase('setup'); $('#draw-button').disabled = false; $('#card-status').textContent = '尚未抽牌'; }

if (typeof document !== 'undefined') {
  renderThemeOptions(); renderHistory(); setPhase('setup');
  document.addEventListener('click', event => {
    const target = event.target.closest('[data-theme], [data-mood], [data-action], [data-followup]');
    if (!target) return;
    if (target.dataset.theme) { state.theme = target.dataset.theme; renderThemeOptions(); }
    if (target.dataset.mood) { state.mood = target.dataset.mood; renderThemeOptions(); }
    if (target.dataset.action === 'draw') draw();
    if (target.dataset.action === 'reset') reset();
    if (target.dataset.followup) showReading(target.dataset.followup);
  });
}
