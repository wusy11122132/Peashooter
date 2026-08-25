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
  { id: 'hanged-man', name: '倒吊人', number: 'XII', symbol: 'XII', keywords: '暂停 · 换位 · 放下', upright: '暂时不动也是一种行动。换一个角度，你会看见原本被惯性遮住的东西。', reversed: '等待可能已经变成拖延。问问自己，你是在观察，还是害怕承担选择。', themes: { love: '放下想立刻得到答案的执着，先看看关系真正需要什么。', work: '换一个方法或顺序，暂停并不代表失去进度。', mood: '允许自己今天不解决全部问题，恢复视角本身就很重要。', future: '有些门必须等你改变看法后才会打开。', open: '你不一定需要更多力气，也许需要换一个方向看。' }, actions: ['暂缓一个冲动决定，给它一个晚上。', '从对立面的角度重新描述当前问题。'] },
  { id: 'death', name: '死神', number: 'XIII', symbol: 'XIII', keywords: '结束 · 转化 · 重生', upright: '某个旧阶段正在结束，为新的形态让出位置。结束不是惩罚，而是转化的入口。', reversed: '你可能还在抓住已经完成的章节。松开一点，变化才有空间发生。', themes: { love: '旧的相处方式需要结束，关系才可能以新的形态继续。', work: '放下不再有效的方法，为下一阶段腾出空间。', mood: '允许一种情绪结束，不必把它带进明天。', future: '变化正在发生，先告别，再迎接。', open: '有些门只有在你转身告别后才会出现。' }, actions: ['清理一件已经不再服务于你的东西。', '写下你愿意结束的一个旧循环。'], annotation: '骷髅并非死亡的恐吓，而是所有人都会经过的转化。'
  },
  { id: 'temperance', name: '节制', number: 'XIV', symbol: 'XIV', keywords: '调和 · 平衡 · 流动', upright: '不同的部分正在找到合适的比例。慢一点，让事情自然混合，而不是急着定型。', reversed: '生活的某个部分正在失衡。不是要更用力，而是要重新分配你的注意力。', themes: { love: '关系需要耐心调和，不必每次都立刻得到结论。', work: '把不同能力和节奏放在一起，稳定会带来效率。', mood: '让休息和行动轮流出现，恢复不是浪费时间。', future: '答案正在慢慢融合，急促会让你错过中间的颜色。', open: '今天的关键词不是更多，而是刚刚好。' }, actions: ['给今天的安排留出一段缓冲时间。', '把两个看似冲突的需求各满足一半。'], annotation: '天使将水在两只杯子间流动，象征内在与外在的调和。'
  },
  { id: 'devil', name: '恶魔', number: 'XV', symbol: 'XV', keywords: '欲望 · 束缚 · 阴影', upright: '看见让你上瘾的东西，才有机会重新选择。欲望本身不必被羞耻覆盖。', reversed: '某条束缚正在松动。你比想象中更有能力说“不”。', themes: { love: '辨认依赖、占有与真正的亲密，不要把强烈误认为深刻。', work: '注意那些让你持续消耗却不再有意义的交换。', mood: '不要因为有阴影就责怪自己，先承认它的存在。', future: '自由通常从看清自己被什么牵引开始。', open: '你可以喜欢某样东西，也可以不再被它控制。' }, actions: ['记录一次让你失去选择感的时刻。', '给一个消耗性的习惯设置一个小边界。'], annotation: '锁链是松的，提示束缚并非不可改变；真正的钥匙是觉察。'
  },
  { id: 'tower', name: '高塔', number: 'XVI', symbol: 'XVI', keywords: '震动 · 真相 · 重建', upright: '某个不稳固的结构正在被看见。剧烈的变化也可能把你带回真实。', reversed: '你可能在延迟一场必要的改变。小范围拆除，胜过等它自然崩塌。', themes: { love: '坦诚可能打破假象，但真实比维持表面的平静更有价值。', work: '旧方案需要重做，先保住核心，再重建结构。', mood: '情绪的震动在提醒你：某种压抑已经太久。', future: '变化会带来空白，也会带来重新选择的空间。', open: '不是所有倒塌都意味着失去，有些只是终于不必再撑。' }, actions: ['找出一个最不稳的假设，重新验证它。', '为意外变化准备一个最小可行的备用方案。'], annotation: '闪电击中高塔，象征突然抵达的真相与被打破的旧秩序。'
  },
  { id: 'star', name: '星星', number: 'XVII', symbol: 'XVII', keywords: '希望 · 疗愈 · 信任', upright: '在经历过波动之后，仍有一小片清澈的希望。你可以重新相信未来。', reversed: '希望没有消失，只是被疲惫挡住了。先恢复，再寻找远方。', themes: { love: '真诚和温柔正在恢复连接，不必急着证明一切。', work: '让愿景重新成为方向，而不是只盯着眼前的消耗。', mood: '你值得被安静地照顾，恢复本身就是进展。', future: '未来有光，但它需要你持续给自己一点信任。', open: '抬头看一眼，今晚的答案可能不在脚边。' }, actions: ['写下一件你仍然愿意相信的事。', '做一件让未来的自己更容易呼吸的事。'], annotation: '裸身女子将水倒入池中与土地，代表真实、疗愈和不再隐藏。'
  },
  { id: 'moon', name: '月亮', number: 'XVIII', symbol: 'XVIII', keywords: '梦境 · 迷雾 · 直觉', upright: '眼前有迷雾，直觉会比强行下结论更可靠。先承认不确定，再慢慢辨认方向。', reversed: '迷雾正在散去。一个被夸大的恐惧，可能很快会回到它真实的尺寸。', themes: { love: '不要只靠猜测填补空白，温柔地确认比反复想象更有帮助。', work: '信息还不完整，暂缓做不可逆的决定。', mood: '梦和情绪都在说话，但它们不一定是事实本身。', future: '未来暂时不清楚，并不代表它正在变坏。', open: '今晚适合相信感觉，但记得明天再核对事实。' }, actions: ['把“我知道”和“我猜测”分成两栏。', '给一个反复出现的梦或念头记下关键词。'], annotation: '月亮照着两座塔和一条道路，代表意识与未知之间的过渡。'
  },
  { id: 'sun', name: '太阳', number: 'XIX', symbol: 'XIX', keywords: '清晰 · 喜悦 · 活力', upright: '事情正在变得清楚。允许自己享受已经获得的光亮，不必立刻寻找下一个问题。', reversed: '喜悦被一层疲惫遮住了，但它仍然存在。别用完美标准否定已经发生的好事。', themes: { love: '坦率的快乐会让关系变得明亮，今天适合表达欣赏。', work: '成果值得被看见，清楚地展示你的贡献。', mood: '让身体接触一点阳光、空气或真正喜欢的东西。', future: '前方有更清楚的道路，继续诚实地走。', open: '今天可以开心，不需要先证明自己配得上。' }, actions: ['把一个已经完成的成果认真记下来。', '主动分享一次真实的开心。'], annotation: '孩子骑马走向太阳，象征未经防御的生命力与清澈的自我表达。'
  },
  { id: 'judgement', name: '审判', number: 'XX', symbol: 'XX', keywords: '觉醒 · 回应 · 重生', upright: '一个旧问题正在呼唤你的回应。你已经拥有重新选择的机会。', reversed: '别人的声音盖过了自己的召唤。你不需要通过自我惩罚来证明已经成长。', themes: { love: '诚实回望过去，关系才有机会脱离旧剧本。', work: '回顾经验，承认真正想回应的方向。', mood: '不要只评价自己，也听听内心在召唤什么。', future: '一个新的阶段正在敲门，回应它需要勇气。', open: '你已经醒来一部分了，接下来要不要回应？' }, actions: ['给过去的自己写一句不带责备的话。', '重新回答一个你曾经逃避的问题。'], annotation: '号角唤醒沉睡者，象征觉察、复盘与第二次机会。'
  },
  { id: 'world', name: '世界', number: 'XXI', symbol: 'XXI', keywords: '完成 · 圆满 · 新循环', upright: '一个循环正在完成。请承认自己走了很远，然后带着所得进入下一章。', reversed: '还有一个小小的收尾没有完成。不要因为接近终点就忽略最后一步。', themes: { love: '一段关系进入新的完整阶段，也许是确认，也许是释然。', work: '阶段性成果值得庆祝，完成会为下一次出发腾出空间。', mood: '你不需要再变成另一个人，先看见现在已经拥有的自己。', future: '旧地图即将收起，新的旅程会从完成感中开始。', open: '这一圈走完了，下一圈会带你去哪里？' }, actions: ['完成一件拖延已久的小收尾。', '为这段旅程写下三个你真正学到的东西。'], annotation: '花环中的舞者代表完成与循环，四角的守护者对应世界的四种力量。'
  }
];

const defaultAnnotations = {
  fool: '悬崖边的旅人带着小包出发，象征未经定义的可能性。', magician: '桌上的四种法器对应四元素，提醒你资源其实已经在手边。', 'high-priestess': '帷幕后的石柱守护内在知识，答案需要在安静中浮现。', empress: '麦田、河流与丰饶的姿态，象征生命正在被滋养。', emperor: '石座与山脉构成秩序，代表边界、结构和承担责任。', hierophant: '两位侍者在教皇面前学习，象征传统、传承与被验证的方法。', lovers: '两人站在选择之前，背后的树与蛇提醒价值观会塑造关系。', chariot: '两只方向不同的狮身兽由同一位车夫驾驭，代表意志的统一。', strength: '女子以温柔驯服狮子，象征不压抑力量而是与它相处。', hermit: '山顶的灯只照亮下一步，代表独处时逐渐清晰的智慧。', wheel: '轮盘不断转动，四角的生灵提醒变化中仍有可学习的部分。', justice: '天平与宝剑分别代表衡量和行动，诚实需要落实为选择。'
};
cards.forEach(card => { if (!card.annotation) card.annotation = defaultAnnotations[card.id] || '牌面中的象征彼此呼应，邀请你从不同角度观察当下。'; });
cards.forEach(card => { card.arcana = 'major'; });

const suitDefinitions = [
  { suit: '权杖', element: '火', symbol: '♣', domain: '行动、创造与热情', image: '一束向上生长的权杖', action: '把能量放回一个真正想推进的方向' },
  { suit: '圣杯', element: '水', symbol: '♡', domain: '情绪、关系与直觉', image: '一只盛满水的圣杯', action: '给真实的感受留出被听见的空间' },
  { suit: '宝剑', element: '风', symbol: '⚔', domain: '思想、沟通与决定', image: '一把指向天空的宝剑', action: '把混乱的念头整理成一句清楚的话' },
  { suit: '星币', element: '土', symbol: '◇', domain: '现实、身体与资源', image: '一枚落在土地上的星币', action: '照顾一个具体而现实的需要' }
];
const numberMeanings = [
  ['王牌', '种子 · 开始', '一份新的能量正在出现。先接住它，不必马上要求结果。'],
  ['二', '平衡 · 选择', '两个方向同时出现，调整节奏比急着决定更重要。'],
  ['三', '展开 · 协作', '事情开始长出形状，分享与合作会让它走得更远。'],
  ['四', '稳定 · 休息', '暂时停下来巩固已有的部分，稳定本身也是进展。'],
  ['五', '摩擦 · 变化', '不顺正在暴露需要调整的地方，不必把它等同于失败。'],
  ['六', '给予 · 回应', '某种支持正在流动，留意自己如何给予，也如何接受。'],
  ['七', '考验 · 信念', '你已经走到需要坚持的位置，重新确认为何出发。'],
  ['八', '节奏 · 技艺', '重复会带来熟练，稳定地做下去比寻找捷径更可靠。'],
  ['九', '成熟 · 临界', '成果已经接近完成，先承认走到这里需要的力量。'],
  ['十', '完成 · 负担', '一个循环来到顶点，分担或放下才能为下一轮留出空间。']
];
const courtMeanings = [
  ['侍者', '学习 · 消息', '一种年轻、好奇的能量带来新的消息，也邀请你重新学习。'],
  ['骑士', '行动 · 追寻', '这份能量正在向外移动，方向感比速度更值得留意。'],
  ['王后', '滋养 · 内在掌握', '成熟的感受力正在发挥作用，先理解再引导。'],
  ['国王', '掌握 · 外在表达', '这份能量已经可以承担责任，把经验转化为清晰的行动。']
];

function minorThemes(definition, meaning) {
  return {
    love: `${definition.domain}正在关系中寻找表达。${meaning}`,
    work: `把${definition.domain}放回现实的工作节奏。${meaning}`,
    mood: `留意与你的${definition.element}元素有关的感受。${meaning}`,
    future: `未来会从${definition.domain}的积累中展开。${meaning}`,
    open: `这张牌带来关于${definition.domain}的一点提醒。${meaning}`
  };
}

function createMinorArcana() {
  return suitDefinitions.flatMap(definition => {
    const numberCards = numberMeanings.map(([rank, keywords, meaning], index) => ({
      id: `${definition.suit}-${index + 1}`,
      name: `${definition.suit}${rank}`,
      number: index === 0 ? 'A' : String(index + 1),
      symbol: definition.symbol,
      suit: definition.suit,
      element: definition.element,
      rank,
      rankType: 'number',
      arcana: 'minor',
      keywords: `${keywords} · ${definition.element}`,
      upright: meaning,
      reversed: `这份${keywords.split(' · ')[0]}能量暂时受阻。放慢一点，先确认自己真正需要什么。`,
      themes: minorThemes(definition, meaning),
      actions: [definition.action, '把这张牌的关键词写进今天的一个具体安排。'],
      annotation: `${definition.image}，对应${definition.domain}；${meaning}`
    }));
    const courtCards = courtMeanings.map(([rank, keywords, meaning], index) => ({
      id: `${definition.suit}-${rank}`,
      name: `${definition.suit}${rank}`,
      number: ['P', 'K', 'Q', 'R'][index],
      symbol: definition.symbol,
      suit: definition.suit,
      element: definition.element,
      rank,
      rankType: 'court',
      arcana: 'minor',
      keywords: `${keywords} · ${definition.element}`,
      upright: meaning,
      reversed: `这位${rank}的${keywords.split(' · ')[0]}能量需要重新找到边界，不要急着替别人承担。`,
      themes: minorThemes(definition, meaning),
      actions: [definition.action, `观察一位${rank}式的人如何处理今天的局面。`],
      annotation: `${definition.image}旁出现${rank}的身影，代表${definition.domain}以一种人格化的方式来到你面前。`
    }));
    return [...numberCards, ...courtCards];
  });
}

cards.push(...createMinorArcana());

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

export function getEasterEgg(cardIds = []) {
  const ids = new Set(cardIds);
  if (ids.has('star') && ids.has('moon')) return '星星与月亮同时出现：希望和直觉正在同一片夜色里说话。';
  if (ids.has('fool') && ids.has('world')) return '愚者与世界相遇：一段旅程完成了，而新的旅程已经在门外。';
  if (ids.has('death') && ids.has('sun')) return '死神与太阳相遇：结束之后，光会更容易被看见。';
  if (cardIds.length >= 3 && cardIds.every(id => cards.find(card => card.id === id)?.number?.length <= 3)) return '三道象征在此刻交汇，像有一条线悄悄浮现。';
  return '';
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
    keywords: card.keywords,
    annotation: card.annotation
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
  $('#reading-annotation').textContent = reading.annotation;
  const egg = getEasterEgg([...state.history.map(item => item.id), card.id]);
  $('#reading-easter-egg').textContent = egg;
  $('#reading-easter-egg').hidden = !egg;
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
