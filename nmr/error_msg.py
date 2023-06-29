import re

error_messages = [
    "#TotalReturnSwapLegCore: YieldCurveName should be a valid curve(KCurve KRO.KCurve not found - Object status: KCurveBuild: Currency must be a string) or a valid SpreadCurve(KCurve pvgenx4862y5185-VAR-AS-B3-4862-5186-x65_KRO.KCurve not found - Object status: KCurveBuild: Currency must be a string) but instead was pvgenx4862y5185-VAR-AS-B3-4862-5186-x65_KRO.KCurve!",
    "#TotalReturnSwapLegCore: YieldCurveName should be a valid curve(KCurve KRO.KCurve not found - Object status: KCurveBuild: Currency must be a string) or a valid SpreadCurve(pvgenx4862y5185-VAR-AS-B3-4862-5186-x67_KRO.KCurve) or a valid KCurve(KCurve pvgenx4862y5185-VAR-AS-B3-4862-5186-x67_KRO.KCurve not found - Object status: KCurveBuild: Currency must be a string) but instead was pvgenx4862y5185-VAR-AS-B3-4862-5186-x67 KRO.KCurve!",
    "#TotalReturnSwapLegCore: YieldCurveName should be a valid curve(KCurve KRO.KCurve not found - Object status: KCurveBuild: Currency must be a string) or a valid SpreadCurve(pvgenx4862y5185-VAR-AS-B3-4862-5186-x285_KRO.KCurve) or a valid KCurve(KCurve pvgenx4862y5185-VAR-AS-B3-4862-5186-x285_KRO.KCurve not found - Object status: KCurveBuild: Currency must be a string) but instead was pvgenx4862y5185-VAR-AS-33-4862-5186-x285 KRO.KCurve!",
    "#TotalReturnSwapLegCore: YieldCurveName should be a valid curve(KCurve KRO.KCurve not found - Object status: KCurveBuild: Currency must be a string) or a valid or a valid KCurve(KCurve pvgenx4862y5185-VAR-AS-B3-4862-5186-x66_KRO.KCutve not found - Object status: KCurveBuild: Currency must be a string) but instead was pvgenx4862y5185-VAR-AS-33-4862-5186-x66 KRO.KCurve!"
]

regex_pattern = r"pvgenx[a-zA-Z0-9\-]+_"

processed_messages = []
for message in error_messages:
    processed_message = re.sub(regex_pattern, "", message)
    processed_messages.append(processed_message)

for message in processed_messages:
    print(message)