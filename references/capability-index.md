# 能力索引（完整版）

| capability_id | 标题 | 重要度 | 意图 | 关键词 | 能力卡 |
|---|---|---|---|---|---|
| cap.wenlv-video-prompt.deconstruct | 逆向拆解一条参考片 | high | 拆解一条参考片，搞清楚它怎么拍的；把已有 breakdown/分镜数据整理成可复现报告；复刻前先确认原片的结构、节奏与画面参数；复盘已发布片子，留一份可回查的记录 | 拆解、分镜表、画面基准、制作方式、置信度、deconstruct、shot list、reverse engineer、breakdown | capabilities/deconstruct.md |
| cap.wenlv-video-prompt.story-structure | 叙事结构选型与分段节奏 | high | 这条片子该用什么叙事结构；30 秒/60 秒怎么分段排节奏；一堆素材没有主线，纠结做清单还是讲故事；连续几条片子担心同质化，想换结构 | 叙事结构、分段、节奏、钩子、结构选型、narrative、story structure、beats、pacing | capabilities/story-structure.md |
| cap.wenlv-video-prompt.impact-design | 视觉张力与记忆点设计（反平淡） | high | 用户说"太平淡/没记忆点/不够燃/像PPT"；复刻时怕只抄结构没抄到好看在哪；提示词全对但觉得缺点什么；同一城市连做多条越做越平；交付前查速度曲线与爆点 | 太平淡、没记忆点、不抓人、不够燃、流水账、像PPT、千篇一律、爆点、钩子、速度曲线、反差、视觉张力、flat、boring、no hook、memorable、wow moment | capabilities/impact-design.md |
| cap.wenlv-video-prompt.prompt-pack | 提示词包装配（全局+分镜+负向+双版本） | critical | 把结构写成可直接生成的分镜提示词；补负向提示词，解决字幕/换脸/变形问题；把别人的提示词改成双版本可用格式；估算生成调用次数与成本；有参考图/三视图时排查图文冲突，解决人物站着不动、道具丢失；生成的视频里人物不开口、不看镜头，口播接不上 | 提示词、分镜提示词、负向提示词、生成单元、双版本、prompt、shot prompt、negative prompt、storyboard、口播、对镜头说话、口型、lip-sync、数字人 | capabilities/prompt-pack.md |
| cap.wenlv-video-prompt.city-swap | 换城 / 换人 / 换场景 | critical | 把这份模板换成我们城市/我们的人物；同一结构套到多个城市做系列；客户临时要换主角、换场景、改昼夜；只改局部不想重写全文 | 换城、换人物、槽位、五连槽、替换、city swap、replace character、adapt template、slots | capabilities/city-swap.md |
| cap.wenlv-video-prompt.compliance-rewrite | 合规改写（禁用词 + 客观化三步） | high | 这句话能不能发/会不会违规；把「最美/震撼/必去」改成客观描述；客户给的文案形容词太多，落成可拍画面；交付前做最后一遍合规检查 | 合规、禁用词、广告法、客观化、夸大、compliance、absolute claims、objective rewrite | capabilities/compliance-rewrite.md |
| cap.wenlv-video-prompt.packaging-audio | 包装层与声音设计 | medium | 字幕/花字/文字标注怎么排；换文案后卡点乱了怎么跟着台词走；配乐选不准，要 BPM 区间与段落起伏；交后期需要一份包装规格表 | 包装层、字幕、花字、文字标注、卡点、BPM、packaging、subtitle、sound design | capabilities/packaging-audio.md |
