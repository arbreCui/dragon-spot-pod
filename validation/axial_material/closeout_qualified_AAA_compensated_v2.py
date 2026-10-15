"""Seal the actual AAA outcome and its source record; never promote a failure."""
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
ART = ROOT / "validation/artifacts"
PRODUCTION = ART / "axial-material-production-qualified-AB-compensated-20261004"
sys.path.insert(0, str(PRODUCTION / "runtime"))
from production_runner import DiskResources, require_file, sha256, verify_prepared, verify_sealed_directory
from qualified_snapshot_ingestion import descriptor


def write_new(path, value):
    with path.open("x") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main():
    ce = ART / "axial-material-ce-qualified-AB-compensated-20261004/AAA"
    admission = ART / "axial-material-qualified-AB-compensated-admission-20261004"
    observations = ART / "axial-material-qualified-AAA-observables-20261004"
    candidate = ART / "axial-material-AAA-compensated-flight-20261004"
    out = ART / "axial-material-AAA-compensated-closeout-20261004"
    prepared = verify_prepared(PRODUCTION / "prepared.json", "2992e4475e0794a6505517fb252c4ee8dac281e7aefafb0f808792813cb1a0d7")
    status = json.loads((PRODUCTION / "AAA/run_status.json").read_text())
    claim = json.loads((PRODUCTION / "AAA/run_claim.json").read_text())
    assessment = json.loads((ce / "reference_assessment.json").read_text())
    stats = json.loads((ce / "statistics.json").read_text())
    currents = json.loads((ce / "currents_balance_symmetry.json").read_text())
    native = json.loads((ce / "native_result.json").read_text())
    analyses = json.loads((ce / "analysis_result.json").read_text())
    if (analyses["classification"] != "COMPLETE_REFERENCE_ANALYSIS"
            or analyses["reference_assessment_sha256"] != sha256(ce / "reference_assessment.json")):
        raise ValueError("complete frozen reference assessment required")
    for pin in assessment["evidence"].values():
        require_file(Path(pin["path"]), pin["sha256"])
    for directory in (PRODUCTION / "archives", PRODUCTION / "training", PRODUCTION / "AAA/bootstrap"):
        verify_sealed_directory(directory)
    maps = status["cases"]["AAA"]["maps"]
    for row in maps:
        verify_sealed_directory(PRODUCTION / "AAA" / f"map{row['epoch']:03d}")
    for folder, digest in (("axial-material-r64-A-qualified-20261003", "74fbca143d0a4909e21e40a4ec9227990e6c6f13956f595e17bc94ed010868bf"),
            ("axial-material-r64-B-qualified-20261004", "10040344aabc32c9516575534928e4ab203ae7d2a7849ee0c9dd4f9cd4311cb8")):
        seal = require_file(ART / folder / "result.sha256", digest)
        for line in seal.read_text().splitlines():
            expected, name = line.split("  ", 1)
            require_file(seal.parent / name, expected)
    out.mkdir(exist_ok=True)
    if (out / "REPORT.txt").exists() or (out / "verification.json").exists():
        raise ValueError("existing closeout: no overwrite")
    source_record = out / "source_record"
    source_record.mkdir()
    tools = ROOT / "validation/axial_material"
    sources = {name: tools / name for name in (
        "prepare_qualified_AB_compensated_production.py", "review_qualified_AB_input_identity_compensated.py",
        "prepare_qualified_AB_ce_reference_compensated.py", "export_qualified_AAA_observables_compensated.py",
        "admit_qualified_AAA_ce_compensated.py", "reference_statistics.py", "compare_balance_symmetry.py",
        "assess_qualified_AAA_reference_compensated.py", "run_qualified_AAA_reference_analysis_compensated.py",
        "plot_qualified_AAA_reference_compensated.py", "plot_qualified_AAA_reference_compensated_v2.py",
        "closeout_qualified_AAA_compensated.py", "closeout_qualified_AAA_compensated_v2.py")}
    sources.update({"candidate_production_runner.py": PRODUCTION / "runtime/production_runner.py",
        "candidate_production_inputs.py": PRODUCTION / "runtime/production_inputs.py",
        "candidate_snapshot_ingestion.py": PRODUCTION / "runtime/qualified_snapshot_ingestion.py",
        "candidate_SPOR64_A8.f90": candidate / "build/SPOR64_A8.f90",
        "candidate_MCGFCF.f": candidate / "build/AXMAT_MCGFCF_COMP.f"})
    for name, source in sources.items():
        shutil.copy2(source, source_record / name)
        require_file(source_record / name, sha256(source))
    evidence = [PRODUCTION / "prepared.json", PRODUCTION / "AAA/run_status.json", PRODUCTION / "AAA/stages.json",
        admission / "input_equivalence_AAA.json", admission / "ce_input_identity.json",
        candidate / "native_flight_source_review.json", candidate / "source_gate_verification.json",
        candidate / "sum_test/result.json", candidate / "compatibility_test/runtime_test_receipt.json",
        observations / "export_receipt.json", observations / "production_checks.json",
        *[observations / f"observables.{name}" for name in ("regions.csv", "faces.csv", "summary.txt")],
        ce / "execution.json", ce / "measurement_admission.json", ce / "native_result.json",
        ce / "statistics.json", ce / "currents_balance_symmetry.json", ce / "reference_assessment.json", ce / "analysis_result.json",
        ce.parent / "analysis_collection_declaration.json", ce.parent / "analysis_driver_declaration.json"]
    aba_started = (PRODUCTION / "ABA/run_claim.json").exists() or (ce.parent / "ABA/run_claim.json").exists()
    if aba_started and not assessment["ABA_admitted"]:
        raise ValueError("unqualified AAA cannot authorize an ABA run")
    verified = dict(schema="AXMAT_COMPLETE_AAA_COMPENSATED_REFERENCE_CLOSEOUT_V1",
        classification=assessment["classification"], production_fixed_point="VALID_MET",
        completed_maps=len(maps), checks=assessment["checks"], independent_AAA_qualified=assessment["ABA_admitted"],
        ABA_started=aba_started, shared_coupled_runtime_promoted=False, new_D4_CE_accuracy_accepted=False,
        input_records={str(path): sha256(path) for path in evidence},
        source_record={name: descriptor(source) for name, source in sources.items()},
        scope="This isolated same-temperature axial pin control is distinct from the repaired D4 component. An original gate failure or inconclusive check is preserved and prohibits ABA admission.")
    k = stats["k"]
    lines = ["2026-10-04：同温轴向针元 AAA 控制验收", "",
        "本轮结果：A/B 离线双精度快照均已通过原门槛；AAA 在第 4 轮达到迭代收敛门槛。",
        "独立参考结论：" + assessment["classification"],
        "ABA：" + ("已准入，实际执行进度见独立 ABA 状态文件。" if assessment["ABA_admitted"] else "未准入；本轮未启动。"), "",
        "这次使用同温、同几何的三段针元控制。A/B 只改变预先选定的燃料组成。",
        "总高 150 cm，三段各 50 cm，12 个轴向单元，8 个径向区域，370 群；径向白边界，轴向真空端面。",
        "A/B/A 共用一次冻结的 rank1 基底；原 rank2 准入失败记录仍保留。此项不是 D4 组件精度验收。", "",
        "AAA 迭代（原阈值三项各 <= 5e-7）：", "轮次       RRHO             RLEAK            RA               状态"]
    lines += [f"{row['epoch']:>2}       {row['defects']['RRHO']:.9e}  {row['defects']['RLEAK']:.9e}  {row['defects']['RA']:.9e}  {row['classification']}" for row in maps]
    lines += ["", f"AAA 全过程：{status['finished_unix'] - claim['started_unix']:.3f} 秒；最终 k = {k['production']:.12f}。",
        "最终保存的双精度通量正值、端面电流方向、共享端面账目伸缩相消、上下镜像对称性均通过。",
        "BOOT 沿用经过精确核验的 REAL32 镜像，然后建立自己的 REAL64 迭代状态；不宣称直接读取离线 FLUX64。",
        "候选修复只改变原径向飞行项的累计方式；深层 1e-13 终值门槛、GMRES 工作上限和全部原物理输入未放宽。",
        "实际编译的累计辅助例和针元/D4 形状兼容性例均通过。候选仅在隔离试验使用，未替换共享运行程序。", "",
        "独立参考：单线程 OpenMC，100 批预热 + 250 批正式统计，每批 50,000 粒子。",
        f"参考全过程：{native['elapsed_seconds']:.3f} 秒；保存 250 个逐批状态点。",
        f"参考 k = {k['reference']:.12f} +/- {k['sigma_k']:.9f}；统计误差 {k['sigma_pcm']:.3f} pcm。",
        f"观察到的反应性差异 {k['reactivity_difference_pcm']:.3f} pcm；原准入额度 {k['allowance_pcm']:.3f} pcm。",
        f"通量形状 L2：点估计 {stats['point_discrepancies'][0]*100:.4f}%，保守 95% 上限 {stats['conservative_upper_95'][0]*100:.4f}%，原目标 1%。",
        f"燃料 nu-fission 最大相对差异：点估计 {stats['point_discrepancies'][1]*100:.4f}%，保守 95% 上限 {stats['conservative_upper_95'][1]*100:.4f}%，原目标 3%。",
        "所有通量、反应率和电流使用每种方法各自唯一的全局 nu-fission 归一化，没有逐层或逐群拟合。", "",
        "完整准入检查："]
    lines += [f"  {name}: {value}" for name, value in assessment["checks"].items()]
    lines += ["", "统计分析总体：" + stats["classification"],
        "未确认项：" + (", ".join(stats["inconclusive_reasons"]) or "无统计不确定项。"),
        "若源历史、区块稳定性或统计分辨率未确认，上述数值只作为诊断结果，不能据此宣称已验收的物理精度。", "",
        "电流：", f"  SPOT/CE 总轴向逃逸除以 nu-fission：{currents['production']['total_escape_per_nufission']:.9e} / {currents['ce']['total_escape_per_nufission']:.9e}。",
        "  保留所有电流符号；跨方法电流只报告差异，没有预先声明的电流精度阈值。",
        "  端面账目相消不等于完整中子平衡；独立吸收/源项未评分，因此完整中子平衡未验收。", "",
        "保留的历史：B 首次打包依赖缺失；首轮 AAA 删除不存在记录；随后累积存储上限；第二轮径向严格内迭代失败。",
        "旧结果未覆盖。失败终态重放定位了 ACA 后残差放大，累计修复后另行声明的完整 AAA 才取得四轮收敛。",
        "原失败目录、原门槛、原核数据、原温度和原材料均保留。独立参考是方法与数据的总差异，不能单独归因于 POD。", "",
        "下一步顺序：先处理未通过或未确认的 AAA 检查并单独声明必要诊断，再完成 AAA 独立准入，最后才运行 ABA。",
        "原方案允许独立的轴向网格或 SN 敏感性试验；敏感性结果不能改写本轮失败或作为逐项误差归因。",
        "完整材料对照 goal 尚不能因这份 AAA 控制报告而标记完成。", "",
        "证据入口：verification.json 中的绝对路径与摘要；source_record 保存本轮分析和隔离运行源代码。",
        "comparison_v2.png / comparison_v2.svg 为有效对照图；comparison.png / comparison.svg 为保留的错误排列展示，已拒绝使用。result.sha256 封存此目录。"]
    with (out / "REPORT.txt").open("x") as stream:
        stream.write("\n".join(lines) + "\n")
    resources = DiskResources(ART, sorted(str(path.resolve()) for path in ART.glob("axial-material-*") if path.is_dir()), 8 * 2**30, 24 * 2**30)
    verified["resources"] = resources.check()
    write_new(out / "verification.json", verified)
    paths = sorted(path for path in out.rglob("*") if path.is_file())
    with (out / "result.sha256").open("x") as stream:
        for path in paths:
            stream.write(f"{sha256(path)}  {path.relative_to(out)}\n")
    print(json.dumps(dict(classification=assessment["classification"], report=str(out / "REPORT.txt"), seal=descriptor(out / "result.sha256")), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
