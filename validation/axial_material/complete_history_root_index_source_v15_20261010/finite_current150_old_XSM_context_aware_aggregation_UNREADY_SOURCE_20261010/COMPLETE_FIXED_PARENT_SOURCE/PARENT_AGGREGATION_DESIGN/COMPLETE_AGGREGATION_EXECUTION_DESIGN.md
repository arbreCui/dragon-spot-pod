# 完整最终 MICROLIB→MACROLIB 聚合：下一实际检查的确定设计

状态：SOURCE_DESIGN_ONLY_UNREADY_NO_AGGREGATION_EXECUTION。本包只读 Source 和既有小 META；不读、解码或 hash 材料 payload，不运行 native、helper、候选、API、guard 或输运。Root 本轮正在做的 persisted-native 检查由 Root 单独观察。本包没有完整聚合 engine、已接线的新 genuine host、实际文件 pins 或运行资格，不能直接执行本包当作完整检查完成。

253项 post-TONE 合同只引用原封存包，不重新授信。新增可执行入口是原生 walker 已保存的 SQLite records 和完整 byte pool；新增确定来源是 TONDRV 的最后两次 MASK/MASKL/ITSTMP 与 SHIBA 存储关系、完整 delayed 分支、presence/FACT/旧字段分支及 LIBDEN 尾部字段生产规则。

## 输入及直接复用

每状态使用一个 `complete_native_original_path_index.sqlite` 与其配对 `complete_native_original_value_bytes.bin`。SQL 精确六列为 `key,ordinal,api_key,row,micro_ordinal,macro_ordinal`；row 是12字段的原生记录描述，含 typed path、kind、declared_count、original_word_count、完整 byte-pool span/hash、原物理 ordinal/slot 和 XSM offset。它不存数值，不存调用历史。数值必须从配对 pool span 取；不能把 XSM offset 当作 pool offset。pool 无 MAGIC；ASCII typed spools 有各自格式，不可混用。SQLite 与 pool 的整文件 pin、所有记录的 span/hash 和实际 native 保存范围三者必须绑定到同一 state/generation。

完整物理 preorder、Ganlib API rank、micro/macro ASCII ordinal 原样保留。禁止按字段名排序后冒充原顺序。原始 type 0=directory(-1)、10=list(count)、99=empty(0)、1=int32、2=REAL32、3=CHAR4 words、4=REAL64(two words)、5=LOGICAL32、6=COMPLEX32(two REAL32 components) 全域都保留。LIBDEN 的 REAL operands 与写出 type2 相匹配；若某被聚合 operand 实际是 type4，记录类型冲突，不能转为 REAL32 后声称原类型一致。未知额外字段通过 complete coverage inventory 保存，不能被白名单丢弃。

本包 data-access adapter 实现 read-only SQL/paired-pool 有界访问、全行顺序 stream、完整 record 流式 hash 和小 context capture。它仅为入口，没有求和、SCAT 聚合或判定全部字段的算法；CLI 明确拒绝运行。作者仅 AST/hash 审查这个 Source，未导入或执行。

## 第一个实际动作：完整上下文 capture，不重读巨型材料

Root 先等待 persisted-native 子进程真实 CLOSED，保留其 honest exit 和完整保存结果。完整 pool/index 可用性按实际 coverage 核实；不能因 ASCII REAL64 loss 或 Source-binlink=false 人为阻断原生 bytes 比较，也不能把 nonzero exit 改为0。需实际独立保存复核和对应 full pins，不能借 raw 软件资格。

Root 的下一完整检查绑定：A/B 每个 SQLite/pool/full-native manifest、实际 closed receipt、独立保存复核、原129输入 provenance、所有当前 Source pins；未知 pins 在模板均为 null。输入整 EOF/SHA7ID 前后验证由 genuine host 负责。adapter 对 SQLite/pool 同样完整 pin 前后验证；原材料 payload 仅原有 input-protection hash，不重解码。新输出、SQL temp、journal、spool、runtime/config、stdout/stderr 全部计 H/O/C/D/E 联合 archive。

从保存 pool 获取如下实际小字段；不从 Source 常数替换 actual values：

- 根 STATE-VECTOR40(kind1)，ISOTOPESUSED/ISOTOPERNAME(kind3,count186，即62×12原bytes)，ISOTOPESMIX(kind1,62)、ISOTOPESDENS/ISOTOPESTEMP(kind2,62)、ISOTOPESSHI(kind1,62)、ISOTOPESLIST(type10,62及全部item/empty)。
- root 与 macro ADDXSNAME-P0(kind3,count36，即18×8bytes)，保持18名称、顺序、重复和前导空格。绝不硬编码为既有12反应。每一个声明名均有独立 presence/branch/coverage 记录，包括 Source 特殊处理名。
- CHI-LIMITS(kind1,5)，macro STATE-VECTOR40、FISSIONINDEX(kind1,64)，SHIBA/STATE-VECTOR40(kind1)及 EPS/TCEPS 原 metadata。SHIBA缺失保持 None；不能用旧审查 Source断言替代实际记录。
- 原 TIMESPER、macro TIMESTAMP、PARTICLE及同伴粒子表、ISOTOPESVOL/MIXTURESVOL、macro SPH、LAMBDA-D 全 presence/type/count/bytes。未出现为 absence，不造零；较大记录用stream，adapter小capture不代表其内容已全部解释。

LIBIPS 的 alias 空item按完整12字节 USED name，取第一较早且已解析的同名目录。每个62 slot仍用自己的 mix/density/temp，不按别名去重求和。root record数、原 isotope字段和宏观19619全记录由完整 native inventory 回归覆盖；context capture 本身不证明全字段完成。

## 当前最终一致性与历史执行必须分开

TONE.f:153–170 从根 STATE 和 ISOTOPESSHI 取初始 interval/LSHI；TONDRV.f:335–350 在最后聚合设 MASKL[g]=IGRMIN<=g<=IGRMAX，MASK[m]=该 mix 有 LSHI>0 的 isotope，ITSTMP=0；401第二次LIBMIX共用这些输入。420–435 将实际 interval/KSPH/ITRANZ/IPHASE 写入 SHIBA/STATE-VECTOR。因而 SHIBA 是下一 actual context 的直接来源，不能再把能群掩码描述成完全无从读取。

但 TONDRV.f:183–192 会根据实际 tracking MAT 删除几何不存在 mix 的 LSHI，且没有回写 ISOTOPESSHI。最终 isotope LSHI只能给候选 mask，actual tracking mixture-presence META/原 deck与log来源链仍须绑定；不能未经证明设所有 mix=true。实际 SHIBA interval 与根索引有可能源自重用 SHIBA/用户输入，不硬套25..281；旧 material audit Source明确曾要求25..281，只引用其历史范围，actual新数据重新读取。

该 TONE 路线 ITSTMP=0。若 actual TIMESPER长度2..6仍存在，LIBDEN.f:135–137按原条件失败；不能强用 TIMFCT=0 静默忽略非法 presence。其他实际聚合路线 ITSTMP/TMPDAY 需真实调用证据；不得自动借 TONE。

MASKK/old macro 存在时，未选mix/group字段继承旧库；完整 final snapshot不是pre-call old macro。不得使用最终值作为旧输入再“自证匹配”。检查所有370×8字段，分别保存 `final_construction_comparison`、`historical_branch_proved`、`historical_old_input_available`。未更新值仍做 current final-micro independent aggregate comparison并完整报告差异；如无法解释继承，标 `HISTORICAL_INPUT_NOT_SAVED` 而非PASS/零。旧 material_audit.py 已区分 P0 scalar resonant band final SIGS与 band外 initial SIGS；不能把全最终 SIGS密度和强迫覆盖这条原规则。

不重新施加 SPH、不设 SPH=1、不补处理来源。final micro本身是聚合输入，SPHfactor/Source→compiled link未证实不阻止做数据实比；它们使历史处理/bit-exact native arithmetic qualification保持false。

## 逐原分支完整算法，给实现者的执行顺序

先写磁盘 coverage 表，每个原 SQL row 一行，含原 typed path/kind/count/span/physical/API/ASCII orders。coverage不是字段白名单；每行必须归入：SOURCE_AGGREGATED / SOURCE_COPIED_METADATA / SOURCE_DERIVED_METADATA / SOURCE_INHERITED_CONTEXT_UNKNOWN / ORIGINAL_PRESENT_NO_AGGREGATION_RULE / ORIGINAL_EMPTY。全部原 payload保存 pin；不解释的字段明确未资格，不删行、不伪称全聚合PASS。再按原 Source顺序处理如下分支。

1. 原62 isotope顺序确定 alias/mix/density、原反应 presence。density==0、null alias、mix==0等源分支各写实际理由；当前scope真实62mix都1..8，若实际偏离，完整report失败而非删 isotope。根 forward IPROB=0需 actual证明；若actual1且NBESP=4，LIBADJ.f:60–61原代码直接拒绝multiple-spectra，不静默转置或补实现。其它实际layout的adjoint需要完整LIBADJ分支。NPART=0/neutron particle需 actual证明；其它粒子完整存储且无 Source规则时标未完成。

2. scalar按 IBM1..8→ISOT1..62→IXSPER 顺序：NTOT0必需；NTOT1有presence才设置全局LWP1；TRANC在实际ITRANC非0时必需且用final micro，不由P1重算。NTOT0/1/TRANC各GA1[g]*DENISO后加accumulator；每轮DENISO*=TIMFCT。STRD以实际LDIFF控制，宏DIFF若非0按1/(3*aggregateSTRD)转换，不能把microSTRD原值直接叫macroDIFF。H-FACTOR/C-FACTOR有presence才写；OVERV密度加权后以基态 TOTDEN 作除法，若全部absence则使用原ENERGY/XDRCST/SQRT fallback。原Utilib/src/XDRCST.f:70给EVJ=1.60217653D-19，109给NMASS=1.67492728D-27；不是替换为当前物理常数。LIBDEN.f:119–121使用double SQFMAS，996–999中ENEAVG为REAL32、ZNU为double后REAL写出；按这些actual source types保留不同sqrt/舍入步骤与未证明compiled linkage。不得凭名称给缺字段零。源代码 accumulator初始化0仅在其确实定义的分支中建 expected accumulator，并记录 Source line与缺项presence；它不是填补材料记录。

3. 全18 extra按原ADDXSNAME顺序。原规则显式跳 NW*、TRANC、BST*/CST*、H-FACTOR。它们仍保留实际每record并指向各自producer/未解释规则，不从coverage移除。普通 CV按mix→iso→IXSPER，LCMLEN=0立即goto720，甚至不会继续后续time suffix；有字段才标 EXIST、按密度累加。DENISO*=TIMFCT只有成功读该suffix时执行。旧macro存在相同CV可使EXIST为真并继承未选mix。全部absent时没有fresh LCMPUT，存在record不能被预期为0。特殊名/额外未声明字段亦保留原bytes及presence。

4. 三矩分别 M1..3，CM='00  '/'01  '/'02  '，源 suffix NORD='    ',' LIN',' QUA'原12字节查找。每矩按 IPASS0..7、50个目标群 slab；最后block只处理351..370。GAR、GAF按源初始化。ISOT1..62顺序，base-density为0才LMADE skip；SIGS[CM+suffix]缺失时原goto130跳本suffix而FACT仍*=TIMFCT；SIGS存在则其 NJJS/IJJS/SCAT均必需。micro sparse index无IPOS：目标群g的IOF0=sum(NJJS[:g-1])，源群从 IJJS[g]倒序连续NJJ项。macro有每mix IPOS，不能误套micro布局。

5. 原 SIGS accumulator加 GA1[dest]*DEN，不乘FACT；SCAT accumulator加 GA2[source,dest]*DEN*FACT。不能将两者都统一权重，更不能以 SCAT列和覆盖 SIGS。按真MASK/MASKK继承未选mix，SIGS写mask由MASKL(dest)或LALL；SCAT写 LOGL 还包括任意 selected source群与非0GAF，不能只检查selected目标群。全370目标×370源×8mix×3矩的数学domain必须覆盖；原稀疏active spans、全部padding、bounds/zero active records与原结构独立保存。

6. compression完全按LIBDEN:430–458：min/max先包含对角dest，再扩展所有非0项，macro每mix IPOS顺序连续。SIGW取实际对角；CHECK[source,mix,moment]按目标群从1..370及descending-source存储顺序累加。全部3矩 CHECK与SIGW都作为独立输出，不用SIGS替代。signed P1/P2不非负化、不乘(2l+1)。active外数学项0只能来自已证明原稀疏表示与Source初始化，不为missing record造0。实际稀疏物理layout与Source compressedlayout不一致按来源/不匹配保存，不能先重压缩native证据掩盖padding差异。

7. FISSIONINDEX原64=8mix×8slot，macro32=8slot×4spectra，绝不补成256index。按actual map绑定isotope ordinal和其own density、alias以及源presence。重建slot分配的历史证明需old FISSIONINDEX/old macro/NFISS0；只靠final64可做mapping-consistency。全macro每group NUSIGF/CHI各256 REAL32按Fortran IOF零基 `((slot-1)*4+(spectrum-1))*8+(mix-1)`。NUSIGF仅实际CHI-LIMITS的源群区间生效；CHI--01..04完整370vector按IXSPER1直接拷贝，不乘density、不重归一、不压成全局chi。LFISS按实际CHI--01中任一>0及NUSIGF presence判定，不由nuclide名猜。

8. STATE(19)=6，完整NUSIGF01..06/CHI01..06每group各256component必须纳入，不能只计prompt32。多谱NESP>1 delayed只在ISP1分支聚合；其余谱组件仍有Source初始化/旧继承规则，实际records全存全比，不能抹去为“unused”。完整保留LIBDEN.f:751的条件 `KFIS.GT.NFISS0*NESP`，不能擅改为直觉上的新slot条件。最后一个 delayed name presence决定整族读入；若其present而中间缺项，原LCMGET应失败，不能按每个独立optional跳过。macroLAMBDA-D完整6×8 REAL32按source_slot/mix循环 last-write及old继承规则，不density平均，不按4spectra重复扩成192。

9. 尾部字段不可漏：macroSTATE40/SIGNATURE/ADDXSNAME-P0/ENERGY/TIMESTAMP/FISSIONINDEX/LAMBDA-D；ISOTOPESVOL→MIXTURESVOL periso last-write→macroVOLUME；NWT0/1→FLUX-INTG(/-P1)为每mix循环最后matching isotope的 vector×VOLMIX，不是62density求和。CHAR/INT/rootdirs/listempty全coverage保留。OVERVfallback、energy末尾0改1e-5、SPH仅presence状态位、PARTICLE copies等源派生 metadata分别报告。BIT不合不能“normalize”。

## REAL32证据，不能偷换成历史机器位资格

每个原 operand同时保留 REAL32 raw bits、Source使用路径和density bits。完整engine必须有独立、已控例验证的binary32 round-to-nearest/even arithmetic；加/乘/除、underflow/subnormal、signedzero/nonfinite/overflow都有明确输出。记录每条Source assignment的 expected32bits、独立binary64 diagnostic、actual32bits/ULP/sign/absolute delta及first mismatch。不得直接Python sum/binary64一次cast取代源ISOT顺序，也不得把重新舍入模型叫原编译程序的已验证每步。

Source表达式只有赋值对象REAL32明确；乘加融合、乘法链临时precision/关联次序和编译options未绑定。因此 `MODEL_SEPARATE_ROUND32` 是明确软件模型：例如 SCAT t1=round32(x*d)，t2=round32(t1*FACT)，sum=round32(sum+t2)；不是编译history proof。独立 high precision/rounding-envelope只诊断可解释差异，不修改3%physical gate、不凭容差授bit-exact。所有 mismatch/loss/nonfinite真实保留，full report落盘后才nonzero；预算/unsafe I/O异常同样诚实失败保存。

## 真正执行与保存复核的顺序

1. Root当前 persisted-native实际关闭与完整saved evidence独立复核，生成actual SQLite/pool/full-native pins；本包不观察其session。
2. 下一作者以此rulebook完成全engine及接线genuinehost，实际context先读小字段再逐原record聚合，不新增native调用或输运。adapter可直接复用，18names与SHIBA等从actualpool取。当前尚无完整engine可执行argv；不能以该adapter CLI冒充完成的checker。
3. 原genuine parent 619/705/38de/bc4/ebbb监督/MRO/check/cleanup全保持；1800whole/600stage/512MiB ownRSS/2GiB jointHOCDE/96GiB history/8GiB free/1thread/1child/0retry。A数据库、pool fd、临时累计与输出全部close后释放，B才open；SQLite cache8MiB/no mmap/temp FILE，one-moment50dest slab，其它仅小62/370context。不预测RSS或时间PASS。
4. future exact argv合同是 `[bound_python, '-B', bound_genuine_host, '--request', actual_request_json, '--output', fresh_O]`，实现时必须与原host接口实际一致。当前各对应pins/null不可自行代填。H/O/C/D/E与allfullinputs真实EOF pins前后；输出包括全coverage.jsonl、scalar/extras/sparse/prompt/delayed/metadata/rounding/missing/context/sourceownership/terminal报告，全部原顺序/字节hash/nativepool引用保存。预算不足不得剪范围或retry。
5. Root实际串行一次运行，独立saved-review完整EOF/schema/pins/streams/guard/RSS/cleanup/alloriginalscope；保留失败report。仅得到最终保存数据聚合一致性证据，不自动授native original LCM RAMbit、Source-binlink、MF6multiplicity、globalbalance、AAA/ABA、科学或新Q。必须另以原独立物理参考继续主线。
