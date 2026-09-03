# 专家评分规则审计

候选严重程度只描述评语被明确提及时的分数条件，不把未提及解释为不存在。
所有规则默认未批准，人工确认 `approved: true` 后才能冻结到 Judge。

## 问题统计

| 问题 | 教师数 | 中位分 | 高分占比 | 低分占比 | 初判 |
| --- | ---: | ---: | ---: | ---: | --- |
| 录音或声音质量问题 | 38 | 3.0717 | 5.3% | 34.2% | context_dependent |
| 教态、表情、目光或动作不足 | 69 | 3.2 | 18.8% | 20.3% | context_dependent |
| 课堂组织或管理不足 | 4 | 3.175 | 25.0% | 25.0% | insufficient_evidence |
| 内容或知识闭环不完整 | 44 | 3.3175 | 38.6% | 18.2% | context_dependent |
| 重点难点、深度或详略不当 | 43 | 3.17 | 9.3% | 25.6% | context_dependent |
| 感染力、激情或生动性不足 | 49 | 3.175 | 16.3% | 24.5% | context_dependent |
| 表达不清、不准确或冗余 | 18 | 3.22 | 5.6% | 27.8% | context_dependent |
| 讲解不够熟练或流畅 | 17 | 3.1 | 11.8% | 23.5% | context_dependent |
| 学科前沿融入不足 | 2 | 3.26 | 0.0% | 0.0% | insufficient_evidence |
| 教学目标或本节定位不清 | 74 | 3.1867 | 17.6% | 24.3% | context_dependent |
| 启发或思维引导不足 | 107 | 3.2 | 32.7% | 14.9% | context_dependent |
| 课堂互动不足 | 151 | 3.2667 | 28.5% | 11.9% | context_dependent |
| 内容组织、衔接或逻辑不清 | 45 | 3.18 | 26.7% | 26.7% | context_dependent |
| 其他尚未归类问题 | 98 | 3.2325 | 31.6% | 20.4% | context_dependent |
| 语速、节奏或时间控制不当 | 62 | 3.18 | 17.7% | 30.6% | context_dependent |
| 课件、板书与讲授配合不足 | 53 | 3.175 | 20.8% | 18.9% | context_dependent |
| 课件文字或信息过载 | 14 | 3.1633 | 7.1% | 28.6% | context_dependent |
| 课件布局、字号或可读性不足 | 27 | 3.14 | 7.4% | 25.9% | context_dependent |
| 理论联系实际不足 | 16 | 3.16 | 0.0% | 31.2% | context_dependent |
| 问题设计不足 | 63 | 3.35 | 38.1% | 7.9% | context_dependent |
| 照读课件或看稿过多 | 17 | 3.02 | 0.0% | 41.2% | context_dependent |
| 总结或收束不足 | 100 | 3.35 | 34.0% | 14.0% | context_dependent |
| 画面、机位或拍摄质量问题 | 45 | 3.1 | 17.8% | 35.6% | context_dependent |

## 待审核规则

- [ ] `audio_quality_rule` 若为 minor_when，仅作为改进建议或在 recording_only 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 recording_only 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `bearing_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_attitude 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_attitude 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `content_incomplete_rule` 若为 minor_when，仅作为改进建议或在 teaching_content 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_content 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `depth_or_focus_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_content 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_content 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `engagement_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `expression_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `fluency_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_quality 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_quality 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `goal_unclear_rule` 若为 minor_when，仅作为改进建议或在 teaching_content 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_content 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `inspiration_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `interaction_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `logic_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_content 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_content 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `other_teaching_aids_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `pace_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `ppt_blackboard_coordination_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `ppt_overloaded_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `ppt_readability_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_quality 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_quality 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `questioning_weak_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `read_slides_rule` 若为 minor_when，仅作为改进建议或在 teaching_method 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 teaching_method 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
- [ ] `video_quality_rule` 若为 minor_when，仅作为改进建议或在 recording_only 维度轻微扣分，不可作为导致该维度低于70分的唯一理由；若为 major_when，在 recording_only 维度作为主要缺陷进行显著扣分，允许导致该维度低于70分。
