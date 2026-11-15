import streamlit as st
import pandas as pd
import json

# Configuration of the Streamlit page
st.set_page_config(
    page_title="Astrofarming — Satellite Telemetry",
    page_icon="🛰️",
    layout="wide"
)

# Calibrated dataset of Magdalena Medio Valley (Santander, Colombia)
ASTROFARMING_RECORDS = [
    {
        "id": 1,
        "Region": "Magdalena Medio Valley (Santander)",
        "Climate_Season": "Dry Season (Jan - Feb)",
        "Short_Season": "Dry Season",
        "Dominant_Soil_Type": "Alluvial Clay-Loam",
        "Soil_Wetness_GWETTOP_pct": 67.5,
        "Air_Temp_T2M_C": 26.3,
        "Precipitation_PRECTOTCORR_mm_month": 58,
        "Solar_Irradiance_MJ_m2_day": 18.1,
        "NASA_POWER_Diagnostic": "Low Rainfall Alert (NASA POWER: 58 mm/mo, Solar 18.1 MJ/m²/d): High evapotranspiration risk for citrus & cacao.",
        "Rotation_Strategy": "1. Traditional (Baseline)",
        "Farmer_Priority": "Maximize short-term yield",
        "Crop_Sequence": "Oil Palm / Citrus (Monoculture)",
        "Water_Consumption_m3_ha": 5200,
        "Nitrogen_Input_kg_ha": 15,
        "Yield_Index_0_100": 85,
        "Soil_Health_Score_0_100": 38,
        "Actionable_Recommendation": "High water demand during dry months; increases soil compaction and requires heavy chemical fertilization."
    },
    {
        "id": 2,
        "Region": "Magdalena Medio Valley (Santander)",
        "Climate_Season": "Dry Season (Jan - Feb)",
        "Short_Season": "Dry Season",
        "Dominant_Soil_Type": "Alluvial Clay-Loam",
        "Soil_Wetness_GWETTOP_pct": 67.5,
        "Air_Temp_T2M_C": 26.3,
        "Precipitation_PRECTOTCORR_mm_month": 58,
        "Solar_Irradiance_MJ_m2_day": 18.1,
        "NASA_POWER_Diagnostic": "Low Rainfall Alert (NASA POWER: 58 mm/mo, Solar 18.1 MJ/m²/d): High evapotranspiration risk for citrus & cacao.",
        "Rotation_Strategy": "2. Soil Health (Legumes)",
        "Farmer_Priority": "Restore soil nutrients",
        "Crop_Sequence": "Cacao / Citrus + Kudzu & Canavalia",
        "Water_Consumption_m3_ha": 3600,
        "Nitrogen_Input_kg_ha": 72,
        "Yield_Index_0_100": 82,
        "Soil_Health_Score_0_100": 89,
        "Actionable_Recommendation": "Legume intercropping fixes natural nitrogen and shades the topsoil, buffering heat stress on mandarin and orange orchards."
    },
    {
        "id": 3,
        "Region": "Magdalena Medio Valley (Santander)",
        "Climate_Season": "Dry Season (Jan - Feb)",
        "Short_Season": "Dry Season",
        "Dominant_Soil_Type": "Alluvial Clay-Loam",
        "Soil_Wetness_GWETTOP_pct": 67.5,
        "Air_Temp_T2M_C": 26.3,
        "Precipitation_PRECTOTCORR_mm_month": 58,
        "Solar_Irradiance_MJ_m2_day": 18.1,
        "NASA_POWER_Diagnostic": "Low Rainfall Alert (NASA POWER: 58 mm/mo, Solar 18.1 MJ/m²/d): High evapotranspiration risk for citrus & cacao.",
        "Rotation_Strategy": "3. Water Resilience (Cover Crops)",
        "Farmer_Priority": "Save water (Drought protection)",
        "Crop_Sequence": "Maize / Sorghum -> Crotalaria Cover",
        "Water_Consumption_m3_ha": 2300,
        "Nitrogen_Input_kg_ha": 50,
        "Yield_Index_0_100": 76,
        "Soil_Health_Score_0_100": 86,
        "Actionable_Recommendation": "Optimal for dry season NASA alerts: reduces surface evaporation and preserves root-zone moisture."
    },
    {
        "id": 4,
        "Region": "Magdalena Medio Valley (Santander)",
        "Climate_Season": "Wet Season (Oct - Nov)",
        "Short_Season": "Wet Season",
        "Dominant_Soil_Type": "Alluvial Clay-Loam",
        "Soil_Wetness_GWETTOP_pct": 78.5,
        "Air_Temp_T2M_C": 24.5,
        "Precipitation_PRECTOTCORR_mm_month": 193,
        "Solar_Irradiance_MJ_m2_day": 16.5,
        "NASA_POWER_Diagnostic": "High Soil Saturation Alert (NASA POWER GWETTOP 78.5%, Rain 193 mm/mo): High runoff & nutrient leaching risk.",
        "Rotation_Strategy": "1. Traditional (Baseline)",
        "Farmer_Priority": "Maximize short-term yield",
        "Crop_Sequence": "Oil Palm / Rubber (Bare Inter-row)",
        "Water_Consumption_m3_ha": 4100,
        "Nitrogen_Input_kg_ha": 18,
        "Yield_Index_0_100": 88,
        "Soil_Health_Score_0_100": 35,
        "Actionable_Recommendation": "Heavy October-November rains wash away topsoil nutrients on exposed slopes, degrading long-term fertility."
    },
    {
        "id": 5,
        "Region": "Magdalena Medio Valley (Santander)",
        "Climate_Season": "Wet Season (Oct - Nov)",
        "Short_Season": "Wet Season",
        "Dominant_Soil_Type": "Alluvial Clay-Loam",
        "Soil_Wetness_GWETTOP_pct": 78.5,
        "Air_Temp_T2M_C": 24.5,
        "Precipitation_PRECTOTCORR_mm_month": 193,
        "Solar_Irradiance_MJ_m2_day": 16.5,
        "NASA_POWER_Diagnostic": "High Soil Saturation Alert (NASA POWER GWETTOP 78.5%, Rain 193 mm/mo): High runoff & nutrient leaching risk.",
        "Rotation_Strategy": "2. Soil Health (Legumes)",
        "Farmer_Priority": "Restore soil nutrients",
        "Crop_Sequence": "Cacao + Mucuna / Perennial Peanut",
        "Water_Consumption_m3_ha": 3100,
        "Nitrogen_Input_kg_ha": 78,
        "Yield_Index_0_100": 86,
        "Soil_Health_Score_0_100": 92,
        "Actionable_Recommendation": "Ideal for wet season: biological nitrogen fixation thrives with soil moisture while living mulch prevents nutrient leaching."
    },
    {
        "id": 6,
        "Region": "Magdalena Medio Valley (Santander)",
        "Climate_Season": "Wet Season (Oct - Nov)",
        "Short_Season": "Wet Season",
        "Dominant_Soil_Type": "Alluvial Clay-Loam",
        "Soil_Wetness_GWETTOP_pct": 78.5,
        "Air_Temp_T2M_C": 24.5,
        "Precipitation_PRECTOTCORR_mm_month": 193,
        "Solar_Irradiance_MJ_m2_day": 16.5,
        "NASA_POWER_Diagnostic": "High Soil Saturation Alert (NASA POWER GWETTOP 78.5%, Rain 193 mm/mo): High runoff & nutrient leaching risk.",
        "Rotation_Strategy": "3. Water Resilience (Cover Crops)",
        "Farmer_Priority": "Prevent erosion and runoff",
        "Crop_Sequence": "Citrus (Mandarin/Lemon) + Brachiaria Cover",
        "Water_Consumption_m3_ha": 2600,
        "Nitrogen_Input_kg_ha": 54,
        "Yield_Index_0_100": 81,
        "Soil_Health_Score_0_100": 90,
        "Actionable_Recommendation": "Recommended under heavy rainfall alerts: dense root networks anchor alluvial soils and improve water infiltration."
    },
    {
        "id": 7,
        "Region": "Magdalena Medio Valley (Santander)",
        "Climate_Season": "Transition Season (Jul - Aug)",
        "Short_Season": "Transition Season",
        "Dominant_Soil_Type": "Alluvial Clay-Loam",
        "Soil_Wetness_GWETTOP_pct": 70.5,
        "Air_Temp_T2M_C": 25.8,
        "Precipitation_PRECTOTCORR_mm_month": 126,
        "Solar_Irradiance_MJ_m2_day": 17.3,
        "NASA_POWER_Diagnostic": "Balanced Moisture Regime (NASA POWER GWETTOP 70.5%, Rain 126 mm/mo): Optimal window for crop rotation planting.",
        "Rotation_Strategy": "1. Traditional (Baseline)",
        "Farmer_Priority": "Maximize short-term yield",
        "Crop_Sequence": "Maize -> Cassava (Sequential)",
        "Water_Consumption_m3_ha": 4400,
        "Nitrogen_Input_kg_ha": 20,
        "Yield_Index_0_100": 86,
        "Soil_Health_Score_0_100": 42,
        "Actionable_Recommendation": "Standard regional rotation; moderate yield but depletes organic matter without legume integration."
    },
    {
        "id": 8,
        "Region": "Magdalena Medio Valley (Santander)",
        "Climate_Season": "Transition Season (Jul - Aug)",
        "Short_Season": "Transition Season",
        "Dominant_Soil_Type": "Alluvial Clay-Loam",
        "Soil_Wetness_GWETTOP_pct": 70.5,
        "Air_Temp_T2M_C": 25.8,
        "Precipitation_PRECTOTCORR_mm_month": 126,
        "Solar_Irradiance_MJ_m2_day": 17.3,
        "NASA_POWER_Diagnostic": "Balanced Moisture Regime (NASA POWER GWETTOP 70.5%, Rain 126 mm/mo): Optimal window for crop rotation planting.",
        "Rotation_Strategy": "2. Soil Health (Legumes)",
        "Farmer_Priority": "Restore soil nutrients",
        "Crop_Sequence": "Maize -> Cowpea / Tropical Bean",
        "Water_Consumption_m3_ha": 3200,
        "Nitrogen_Input_kg_ha": 70,
        "Yield_Index_0_100": 84,
        "Soil_Health_Score_0_100": 88,
        "Actionable_Recommendation": "Takes advantage of balanced mid-year moisture to rebuild soil nitrogen ahead of the October rains."
    },
    {
        "id": 9,
        "Region": "Magdalena Medio Valley (Santander)",
        "Climate_Season": "Transition Season (Jul - Aug)",
        "Short_Season": "Transition Season",
        "Dominant_Soil_Type": "Alluvial Clay-Loam",
        "Soil_Wetness_GWETTOP_pct": 70.5,
        "Air_Temp_T2M_C": 25.8,
        "Precipitation_PRECTOTCORR_mm_month": 126,
        "Solar_Irradiance_MJ_m2_day": 17.3,
        "NASA_POWER_Diagnostic": "Balanced Moisture Regime (NASA POWER GWETTOP 70.5%, Rain 126 mm/mo): Optimal window for crop rotation planting.",
        "Rotation_Strategy": "3. Water Resilience (Cover Crops)",
        "Farmer_Priority": "Save water (Drought protection)",
        "Crop_Sequence": "Citrus + Green Manure Cover",
        "Water_Consumption_m3_ha": 2500,
        "Nitrogen_Input_kg_ha": 48,
        "Yield_Index_0_100": 79,
        "Soil_Health_Score_0_100": 85,
        "Actionable_Recommendation": "Prepares soil structure and organic matter retention before seasonal climate shifts."
    }
]

records_json = json.dumps(ASTROFARMING_RECORDS)

astrofarming_ui = f"""
<div id="astrofarming-root" style="font-family: 'Inter', system-ui, -apple-system, sans-serif; background:#0A0D0C; color:#F3F4F6; border-radius:16px; border:1px solid #222C28; overflow:hidden; margin:8px 0; box-shadow:0 20px 45px rgba(0,0,0,0.65);">
  <style>
    #astrofarming-root * {{ box-sizing: border-box; }}
    .af-header {{ display:flex; flex-wrap:wrap; align-items:center; justify-content:space-between; padding:14px 24px; background:#0E1311; border-bottom:1px solid #222C28; gap:12px; }}
    .af-brand {{ display:flex; align-items:center; gap:10px; font-weight:700; font-size:16px; color:#FFFFFF; }}
    .af-logo {{ width:30px; height:30px; border-radius:8px; background:rgba(16,185,129,0.15); border:1px solid rgba(16,185,129,0.45); display:flex; align-items:center; justify-content:center; color:#10B981; font-size:15px; }}
    .af-nav {{ display:flex; gap:6px; flex-wrap:wrap; }}
    .af-tab {{ padding:7px 14px; border-radius:8px; font-size:13px; font-weight:500; cursor:pointer; border:1px solid transparent; background:transparent; color:#9CA3AF; transition:all .15s; }}
    .af-tab:hover {{ color:#F3F4F6; background:rgba(255,255,255,0.05); }}
    .af-tab.active {{ background:rgba(16,185,129,0.16); color:#10B981; border-color:rgba(16,185,129,0.35); font-weight:600; }}
    .af-body {{ padding:24px; }}
    .af-badge-amber {{ display:inline-block; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:600; background:rgba(245,158,11,0.15); color:#FBBF24; border:1px solid rgba(245,158,11,0.35); }}
    .af-badge-sky {{ display:inline-block; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:600; background:rgba(56,189,248,0.15); color:#38BDF8; border:1px solid rgba(56,189,248,0.35); }}
    .af-badge-green {{ display:inline-block; padding:3px 10px; border-radius:999px; font-size:11px; font-weight:600; background:rgba(16,185,129,0.15); color:#34D399; border:1px solid rgba(16,185,129,0.35); }}
    .af-card {{ background:#111614; border:1px solid #222C28; border-radius:12px; padding:18px; transition:all .18s; }}
    .af-card:hover {{ border-color:rgba(16,185,129,0.5); transform:translateY(-2px); }}
    .af-grid-3 {{ display:grid; grid-template-columns:repeat(auto-fit, minmax(270px, 1fr)); gap:16px; }}
    .af-pill {{ padding:6px 14px; border-radius:999px; font-size:12px; font-weight:500; cursor:pointer; border:1px solid #222C28; background:#171E1B; color:#D1D5DB; transition:all .15s; }}
    .af-pill.active {{ background:#10B981; color:#052E16; border-color:#34D399; font-weight:700; }}
    .af-modal-backdrop {{ display:none; position:fixed; inset:0; background:rgba(0,0,0,0.78); z-index:9999; align-items:center; justify-content:center; padding:16px; }}
    .af-modal {{ background:#111614; border:1px solid #2A3631; border-radius:16px; max-width:560px; width:100%; padding:22px; color:#F3F4F6; position:relative; max-height:92vh; overflow-y:auto; }}
    .af-bar-bg {{ height:7px; background:#0A0D0C; border-radius:999px; overflow:hidden; border:1px solid #1F2925; margin-top:4px; }}
    .af-bar-fill {{ height:100%; border-radius:999px; }}
  </style>

  <!-- Header -->
  <div class="af-header">
    <div class="af-brand">
      <div class="af-logo">🛰️</div>
      <span>Astrofarming</span>
      <span style="font-size:11px; color:#10B981; background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.25); padding:2px 8px; border-radius:6px;">MAGDALENA MEDIO • SANTANDER</span>
    </div>
    <div class="af-nav">
      <button id="tab-home" class="af-tab active" onclick="afSwitchTab('home')">Home</button>
      <button id="tab-advisor" class="af-tab" onclick="afSwitchTab('advisor')">Crop Rotation Advisor</button>
      <button id="tab-analytics" class="af-tab" onclick="afSwitchTab('analytics')">Strategy Analytics</button>
    </div>
  </div>

  <div class="af-body">
    <!-- TAB 1: HOME -->
    <div id="af-view-home">
      <div style="max-width:760px; margin-bottom:22px;">
        <div style="font-size:11px; letter-spacing:1.5px; text-transform:uppercase; color:#10B981; font-weight:600;">SATELLITE TELEMETRY &amp; AGRO-CLIMATOLOGY</div>
        <h2 style="font-size:28px; font-weight:700; color:#FFFFFF; margin:6px 0 8px 0;">Welcome to Astrofarming</h2>
        <p style="font-size:14px; color:#9CA3AF; line-height:1.55; margin:0;">
          Astrofarming translates <strong style="color:#E5E7EB;">NASA POWER</strong> climate data and <strong style="color:#E5E7EB;">ESA Copernicus Sentinel</strong> imagery into actionable crop rotation strategies for oil palm, cacao, rubber, and citrus farmers in the <strong style="color:#E5E7EB;">Magdalena Medio Valley (Santander, Colombia)</strong>.
        </p>
      </div>

      <!-- Active Climate Alert Banner -->
      <div class="af-card" style="margin-bottom:24px; background:#111614;">
        <div style="display:flex; flex-wrap:wrap; justify-content:space-between; align-items:center; gap:12px; padding-bottom:14px; border-bottom:1px solid #222C28;">
          <div>
            <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
              <span style="color:#F59E0B; font-size:16px;">⚠️</span>
              <strong style="color:#FFFFFF; font-size:15px;">Active Climate Alert</strong>
              <span id="af-home-season" class="af-badge-amber">Dry Season (Jan - Feb)</span>
            </div>
            <p id="af-home-diag" style="font-size:13px; color:#D1D5DB; margin:6px 0 0 0;">
              Low Rainfall Alert (NASA POWER: 58 mm/mo, Solar 18.1 MJ/m²/d): High evapotranspiration risk for citrus &amp; cacao.
            </p>
          </div>
          <div style="display:flex; gap:4px; background:#0A0D0C; padding:4px; border-radius:8px; border:1px solid #222C28;">
            <button id="hbtn-dry" class="af-pill active" style="padding:4px 10px; font-size:11px;" onclick="afSetTelemetry('Dry Season (Jan - Feb)')">Dry (Jan–Feb)</button>
            <button id="hbtn-wet" class="af-pill" style="padding:4px 10px; font-size:11px;" onclick="afSetTelemetry('Wet Season (Oct - Nov)')">Wet (Oct–Nov)</button>
            <button id="hbtn-trans" class="af-pill" style="padding:4px 10px; font-size:11px;" onclick="afSetTelemetry('Transition Season (Jul - Aug)')">Transition (Jul–Aug)</button>
          </div>
        </div>
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(140px, 1fr)); gap:12px; padding-top:14px; font-size:13px;">
          <div><span style="color:#6B7280; font-size:11px;">PRECIPITATION</span><div id="af-t-rain" style="font-weight:700; color:#FFFFFF; margin-top:2px;">💧 58 mm/mo</div></div>
          <div><span style="color:#6B7280; font-size:11px;">SOIL WETNESS (GWETTOP)</span><div id="af-t-wet" style="font-weight:700; color:#FFFFFF; margin-top:2px;">🌱 67.5%</div></div>
          <div><span style="color:#6B7280; font-size:11px;">AIR TEMP (T2M)</span><div id="af-t-temp" style="font-weight:700; color:#FFFFFF; margin-top:2px;">🌡️ 26.3 °C</div></div>
          <div><span style="color:#6B7280; font-size:11px;">SOLAR IRRADIANCE</span><div id="af-t-solar" style="font-weight:700; color:#FFFFFF; margin-top:2px;">☀️ 18.1 MJ/m²/d</div></div>
        </div>
      </div>

      <!-- Satellite Maps -->
      <h3 style="font-size:18px; font-weight:700; color:#FFFFFF; margin:0 0 4px 0;">Satellite observation layers</h3>
      <p style="font-size:13px; color:#9CA3AF; margin:0 0 14px 0;">Verified Copernicus Land Monitoring & Sentinel satellite rasters for Magdalena Medio corridor.</p>
      
      <div class="af-grid-3">
        <div class="af-card">
          <div style="font-size:10px; color:#F59E0B; font-weight:700; letter-spacing:1px;">COPERNICUS LAND MONITORING SERVICE</div>
          <div style="font-size:16px; font-weight:700; color:#FFFFFF; margin-top:2px;">1) Soil Seasonality &amp; Abundance</div>
          <div style="font-size:12px; color:#9CA3AF; margin-bottom:10px;">DMP 300m (0–210 Dry Matter Index)</div>
          <img src="https://raw.githubusercontent.com/mcuevas6/Astroagricultura/main/activos/soil_dmp.jpg.jpeg" style="width:100%; height:165px; object-fit:cover; border-radius:8px; border:1px solid #222C28;" />
          <p style="font-size:12px; color:#9CA3AF; margin:10px 0 0 0;">
            <strong>Scientific Analysis:</strong> Evaluates 10-day dry matter productivity and soil moisture retention across Santander. Red-yellow gradients identify high drought stress and rapid mineralization on exposed alluvial soils.
          </p>
        </div>

        <div class="af-card">
          <div style="font-size:10px; color:#38BDF8; font-weight:700; letter-spacing:1px;">ESA COPERNICUS SENTINEL-1 IW</div>
          <div style="font-size:16px; font-weight:700; color:#FFFFFF; margin-top:2px;">2) Oil Palm Structural Mapping</div>
          <div style="font-size:12px; color:#9CA3AF; margin-bottom:10px;">C-Band SAR RGB Ratio (Backscatter)</div>
          <img src="https://raw.githubusercontent.com/mcuevas6/Astroagricultura/main/activos/oil_palm.jpg.jpeg" style="width:100%; height:165px; object-fit:cover; border-radius:8px; border:1px solid #222C28;" />
          <p style="font-size:12px; color:#9CA3AF; margin:10px 0 0 0;">
            <strong>Scientific Analysis:</strong> Utilizes all-weather C-band synthetic aperture radar (SAR) backscatter ratios (VV/VH). Distinct textural signatures separate perennial oil palm and rubber plantations from low-stature citrus blocks.
          </p>
        </div>

        <div class="af-card">
          <div style="font-size:10px; color:#10B981; font-weight:700; letter-spacing:1px;">ESA COPERNICUS SENTINEL-2 L2A</div>
          <div style="font-size:16px; font-weight:700; color:#FFFFFF; margin-top:2px;">3) Vegetation Index (NDVI)</div>
          <div style="font-size:12px; color:#9CA3AF; margin-bottom:10px;">Optical Chlorophyll Vigor (B8/B4)</div>
          <img src="https://raw.githubusercontent.com/mcuevas6/Astroagricultura/main/activos/ndvi.jpg.jpeg" style="width:100%; height:165px; object-fit:cover; border-radius:8px; border:1px solid #222C28;" />
          <p style="font-size:12px; color:#9CA3AF; margin:10px 0 0 0;">
            <strong>Scientific Analysis:</strong> High-resolution multispectral optical imagery measuring near-infrared reflectance. Dark green pixels indicate dense photosynthetic canopies and robust chlorophyll absorption in the Magdalena river basin.
          </p>
        </div>
      </div>
    </div>

    <!-- TAB 2: CROP ROTATION ADVISOR -->
    <div id="af-view-advisor" style="display:none;">
      <h2 style="font-size:26px; font-weight:700; color:#FFFFFF; margin:0 0 16px 0;">Crop Rotation Advisor</h2>
      <div style="margin-bottom:14px;">
        <div style="font-size:11px; color:#9CA3AF; font-weight:600; letter-spacing:1px; margin-bottom:8px;">CLIMATE SEASON</div>
        <div id="af-season-pills" style="display:flex; flex-wrap:wrap; gap:8px;"></div>
      </div>
      <div style="margin-bottom:20px;">
        <div style="font-size:11px; color:#9CA3AF; font-weight:600; letter-spacing:1px; margin-bottom:8px;">FARMER PRIORITY</div>
        <div id="af-priority-pills" style="display:flex; flex-wrap:wrap; gap:8px;"></div>
      </div>
      <div id="af-cards-container" class="af-grid-3"></div>
    </div>

    <!-- TAB 3: STRATEGY ANALYTICS -->
    <div id="af-view-analytics" style="display:none;">
      <h2 style="font-size:26px; font-weight:700; color:#FFFFFF; margin:0 0 4px 0;">Strategy Analytics</h2>
      <p style="font-size:13px; color:#9CA3AF; margin:0 0 20px 0;">Averages across all climate seasons, grouped by rotation strategy.</p>
      <div class="af-grid-3">
        <div class="af-card">
          <div style="font-size:15px; font-weight:700; color:#FFFFFF;">Yield Index (0–100)</div>
          <div style="font-size:12px; color:#9CA3AF; margin-bottom:16px;">Higher is better</div>
          <div id="af-chart-yield"></div>
        </div>
        <div class="af-card">
          <div style="font-size:15px; font-weight:700; color:#FFFFFF;">Soil Health Score (0–100)</div>
          <div style="font-size:12px; color:#9CA3AF; margin-bottom:16px;">Higher is better</div>
          <div id="af-chart-soil"></div>
        </div>
        <div class="af-card">
          <div style="font-size:15px; font-weight:700; color:#FFFFFF;">Water Consumption (m³/ha)</div>
          <div style="font-size:12px; color:#9CA3AF; margin-bottom:16px;">Lower is better</div>
          <div id="af-chart-water"></div>
        </div>
      </div>
    </div>
  </div>

  <!-- DETAIL MODAL -->
  <div id="af-modal-bg" class="af-modal-backdrop" onclick="if(event.target.id==='af-modal-bg') afCloseModal()">
    <div class="af-modal">
      <button onclick="afCloseModal()" style="position:absolute; top:14px; right:14px; background:#171E1B; border:1px solid #2A3631; color:#D1D5DB; width:30px; height:30px; border-radius:8px; cursor:pointer;">✕</button>
      <div style="display:flex; align-items:center; gap:8px; flex-wrap:wrap;">
        <span id="m-season" class="af-badge-amber"></span>
        <span id="m-priority" style="font-size:12px; color:#9CA3AF;"></span>
      </div>
      <h3 id="m-strategy" style="font-size:20px; font-weight:700; color:#FFFFFF; margin:8px 0 2px 0;"></h3>
      <div id="m-crops" style="font-size:13px; color:#10B981; font-weight:600; margin-bottom:14px;"></div>

      <div style="background:#0A0D0C; border:1px solid #222C28; border-radius:10px; padding:12px; margin-bottom:14px;">
        <div style="font-size:10px; font-weight:700; color:#10B981; letter-spacing:1px;">● ACTIONABLE RECOMMENDATION</div>
        <p id="m-rec" style="font-size:13px; color:#E5E7EB; margin:6px 0 0 0; line-height:1.45;"></p>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:16px;">
        <div style="background:#171E1B; border:1px solid #222C28; border-radius:10px; padding:10px;">
          <div style="font-size:10px; color:#9CA3AF;">DOMINANT SOIL</div>
          <div id="m-soil" style="font-size:13px; font-weight:700; color:#FFFFFF; margin-top:3px;"></div>
        </div>
        <div style="background:#171E1B; border:1px solid #222C28; border-radius:10px; padding:10px;">
          <div style="font-size:10px; color:#9CA3AF;">SOLAR IRRADIANCE</div>
          <div id="m-solar" style="font-size:13px; font-weight:700; color:#FFFFFF; margin-top:3px;"></div>
        </div>
      </div>

      <div style="font-size:12px; font-weight:700; color:#D1D5DB; margin-bottom:10px;">Key numbers</div>
      <div style="margin-bottom:10px;">
        <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#9CA3AF;">Water consumption</span><strong id="m-w-val"></strong></div>
        <div class="af-bar-bg"><div id="m-w-bar" class="af-bar-fill" style="background:#38BDF8;"></div></div>
      </div>
      <div style="margin-bottom:10px;">
        <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#9CA3AF;">Nitrogen input</span><strong id="m-n-val"></strong></div>
        <div class="af-bar-bg"><div id="m-n-bar" class="af-bar-fill" style="background:#10B981;"></div></div>
      </div>
      <div style="margin-bottom:10px;">
        <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#9CA3AF;">Yield index</span><strong id="m-y-val"></strong></div>
        <div class="af-bar-bg"><div id="m-y-bar" class="af-bar-fill" style="background:#10B981;"></div></div>
      </div>
      <div style="margin-bottom:16px;">
        <div style="display:flex; justify-content:space-between; font-size:12px;"><span style="color:#9CA3AF;">Soil health score</span><strong id="m-h-val"></strong></div>
        <div class="af-bar-bg"><div id="m-h-bar" class="af-bar-fill"></div></div>
      </div>

      <!-- Donut Gauges -->
      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px; padding-top:12px; border-top:1px solid #222C28;">
        <div style="display:flex; align-items:center; gap:10px; background:#0A0D0C; border:1px solid #222C28; border-radius:10px; padding:10px;">
          <svg width="48" height="48" viewBox="0 0 36 36" style="transform:rotate(-90deg);">
            <circle cx="18" cy="18" r="15.5" fill="none" stroke="#1E2723" stroke-width="3.5"/>
            <circle id="g-y-arc" cx="18" cy="18" r="15.5" fill="none" stroke="#10B981" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="97.4" stroke-dashoffset="97.4"/>
          </svg>
          <div><div id="g-y-pct" style="font-size:16px; font-weight:700;"></div><div style="font-size:11px; color:#D1D5DB;">Yield</div><div id="g-y-sub" style="font-size:10px; color:#6B7280;"></div></div>
        </div>
        <div style="display:flex; align-items:center; gap:10px; background:#0A0D0C; border:1px solid #222C28; border-radius:10px; padding:10px;">
          <svg width="48" height="48" viewBox="0 0 36 36" style="transform:rotate(-90deg);">
            <circle cx="18" cy="18" r="15.5" fill="none" stroke="#1E2723" stroke-width="3.5"/>
            <circle id="g-h-arc" cx="18" cy="18" r="15.5" fill="none" stroke="#10B981" stroke-width="3.5" stroke-linecap="round" stroke-dasharray="97.4" stroke-dashoffset="97.4"/>
          </svg>
          <div><div id="g-h-pct" style="font-size:16px; font-weight:700;"></div><div style="font-size:11px; color:#D1D5DB;">Soil health</div><div id="g-h-sub" style="font-size:10px; color:#6B7280;"></div></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const AF_DATA = {records_json};
    let afSeason = 'All';
    let afPriority = 'All';

    function afSwitchTab(t) {{
      ['home','advisor','analytics'].forEach(k => {{
        document.getElementById('af-view-'+k).style.display = (k===t) ? 'block' : 'none';
        document.getElementById('tab-'+k).className = (k===t) ? 'af-tab active' : 'af-tab';
      }});
      if(t==='advisor') afRenderAdvisor();
      if(t==='analytics') afRenderAnalytics();
    }}

    function afSetTelemetry(season) {{
      const d = AF_DATA.find(x => x.Climate_Season === season);
      if(!d) return;
      document.getElementById('af-home-season').textContent = d.Climate_Season;
      document.getElementById('af-home-diag').textContent = d.NASA_POWER_Diagnostic;
      document.getElementById('af-t-rain').textContent = '💧 ' + d.Precipitation_PRECTOTCORR_mm_month + ' mm/mo';
      document.getElementById('af-t-wet').textContent = '🌱 ' + d.Soil_Wetness_GWETTOP_pct.toFixed(1) + '%';
      document.getElementById('af-t-temp').textContent = '🌡️ ' + d.Air_Temp_T2M_C.toFixed(1) + ' °C';
      document.getElementById('af-t-solar').textContent = '☀️ ' + d.Solar_Irradiance_MJ_m2_day.toFixed(1) + ' MJ/m²/d';
      ['hbtn-dry','hbtn-wet','hbtn-trans'].forEach(id => document.getElementById(id).classList.remove('active'));
      const act = season.startsWith('Dry') ? 'hbtn-dry' : season.startsWith('Wet') ? 'hbtn-wet' : 'hbtn-trans';
      document.getElementById(act).classList.add('active');
    }}

    function afBadgeClass(shortSeason) {{
      if(shortSeason==='Dry Season') return 'af-badge-amber';
      if(shortSeason==='Wet Season') return 'af-badge-sky';
      return 'af-badge-green';
    }}

    function afRenderAdvisor() {{
      const seasons = ['All','Dry Season','Wet Season','Transition Season'];
      const priorities = ['All','Maximize short-term yield','Restore soil nutrients','Save water (Drought protection)','Prevent erosion and runoff'];
      document.getElementById('af-season-pills').innerHTML = seasons.map(s => `<button class="af-pill ${{afSeason===s?'active':''}}" onclick="afSeason='${{s}}';afRenderAdvisor()">${{s}}</button>`).join('');
      document.getElementById('af-priority-pills').innerHTML = priorities.map(p => `<button class="af-pill ${{afPriority===p?'active':''}}" onclick="afPriority='${{p}}';afRenderAdvisor()">${{p}}</button>`).join('');

      const list = AF_DATA.filter(x => (afSeason==='All'||x.Short_Season===afSeason) && (afPriority==='All'||x.Farmer_Priority===afPriority));
      document.getElementById('af-cards-container').innerHTML = list.map(x => `
        <div class="af-card" style="cursor:pointer; display:flex; flex-direction:column; justify-content:space-between;" onclick="afOpenModal(${{x.id}})">
          <div>
            <span class="${{afBadgeClass(x.Short_Season)}}">${{x.Climate_Season}}</span>
            <h4 style="font-size:17px; font-weight:700; color:#FFFFFF; margin:10px 0 8px 0;">${{x.Rotation_Strategy}}</h4>
            <div style="font-size:10px; color:#6B7280; font-weight:700;">CROP SEQUENCE</div>
            <div style="font-size:13px; color:#E5E7EB; font-weight:500; margin-top:2px;">${{x.Crop_Sequence}}</div>
          </div>
          <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-top:14px; padding-top:12px; border-top:1px solid #222C28;">
            <div><div style="font-size:10px; color:#6B7280;">SOIL WET.</div><div style="font-size:13px; font-weight:700;">${{x.Soil_Wetness_GWETTOP_pct}}%</div></div>
            <div><div style="font-size:10px; color:#6B7280;">PRECIP.</div><div style="font-size:13px; font-weight:700;">${{x.Precipitation_PRECTOTCORR_mm_month}} mm</div></div>
            <div><div style="font-size:10px; color:#6B7280;">AIR TEMP</div><div style="font-size:13px; font-weight:700;">${{x.Air_Temp_T2M_C}} °C</div></div>
          </div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-top:12px; padding-top:10px; border-top:1px solid #222C28; font-size:12px;">
            <span style="color:#9CA3AF;">${{x.Farmer_Priority}}</span>
            <span style="color:#10B981; font-weight:700;">Details &gt;</span>
          </div>
        </div>
      `).join('');
    }}

    function afOpenModal(id) {{
      const x = AF_DATA.find(d => d.id === id); 
      if(!x) return;
      const sb = document.getElementById('m-season'); 
      sb.textContent = x.Climate_Season; 
      sb.className = afBadgeClass(x.Short_Season);

      document.getElementById('m-priority').textContent = x.Farmer_Priority;
      document.getElementById('m-strategy').textContent = x.Rotation_Strategy;
      document.getElementById('m-crops').textContent = x.Crop_Sequence;
      document.getElementById('m-rec').textContent = x.Actionable_Recommendation;
      document.getElementById('m-soil').textContent = x.Dominant_Soil_Type;
      document.getElementById('m-solar').textContent = x.Solar_Irradiance_MJ_m2_day + ' MJ/m²/d';

      document.getElementById('m-w-val').textContent = x.Water_Consumption_m3_ha + ' m³/ha';
      document.getElementById('m-w-bar').style.width = Math.min(100, (x.Water_Consumption_m3_ha / 6000) * 100) + '%';

      document.getElementById('m-n-val').textContent = x.Nitrogen_Input_kg_ha + ' kg/ha';
      document.getElementById('m-n-bar').style.width = Math.min(100, (x.Nitrogen_Input_kg_ha / 100) * 100) + '%';

      document.getElementById('m-y-val').textContent = x.Yield_Index_0_100 + ' / 100';
      document.getElementById('m-y-bar').style.width = x.Yield_Index_0_100 + '%';

      document.getElementById('m-h-val').textContent = x.Soil_Health_Score_0_100 + ' / 100';
      const hBar = document.getElementById('m-h-bar');
      hBar.style.width = x.Soil_Health_Score_0_100 + '%';
      hBar.style.background = x.Soil_Health_Score_0_100 > 75 ? '#10B981' : x.Soil_Health_Score_0_100 > 50 ? '#FBBF24' : '#EF4444';

      document.getElementById('g-y-pct').textContent = x.Yield_Index_0_100 + '%';
      document.getElementById('g-y-sub').textContent = 'Index';
      const yCirc = 2 * Math.PI * 15.5;
      document.getElementById('g-y-arc').style.strokeDasharray = yCirc;
      document.getElementById('g-y-arc').style.strokeDashoffset = yCirc - (yCirc * x.Yield_Index_0_100 / 100);

      document.getElementById('g-h-pct').textContent = x.Soil_Health_Score_0_100 + '%';
      document.getElementById('g-h-sub').textContent = 'Score';
      document.getElementById('g-h-arc').style.strokeDasharray = yCirc;
      document.getElementById('g-h-arc').style.strokeDashoffset = yCirc - (yCirc * x.Soil_Health_Score_0_100 / 100);

      document.getElementById('af-modal-bg').style.display = 'flex';
    }}

    function afCloseModal() {{
      document.getElementById('af-modal-bg').style.display = 'none';
    }}

    function afRenderAnalytics() {{
      const strategies = [...new Set(AF_DATA.map(x => x.Rotation_Strategy))];
      
      const agg = strategies.map(strat => {{
        const subset = AF_DATA.filter(x => x.Rotation_Strategy === strat);
        const avgYield = subset.reduce((acc, curr) => acc + curr.Yield_Index_0_100, 0) / subset.length;
        const avgSoil = subset.reduce((acc, curr) => acc + curr.Soil_Health_Score_0_100, 0) / subset.length;
        const avgWater = subset.reduce((acc, curr) => acc + curr.Water_Consumption_m3_ha, 0) / subset.length;
        return {{ strat, avgYield, avgSoil, avgWater }};
      }});

      document.getElementById('af-chart-yield').innerHTML = agg.map(item => `
        <div style="margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
            <span style="color:#D1D5DB; font-weight:500;">${{item.strat}}</span>
            <span style="color:#10B981; font-weight:700;">${{item.avgYield.toFixed(1)}}</span>
          </div>
          <div class="af-bar-bg"><div class="af-bar-fill" style="width:${{item.avgYield}}%; background:#10B981;"></div></div>
        </div>
      `).join('');

      document.getElementById('af-chart-soil').innerHTML = agg.map(item => `
        <div style="margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; font-size:12px; margin-bottom:4px;">
            <span style="color:#D1D5DB; font-weight:500;">${{item.strat}}</span>
            <span style="color:#34D399; font-weight:700;">${{item.avgSoil.toFixed(1)}}</span>
          </div>
          <div class="af-bar-bg"><div class="af-bar-fill" style="width:${{item.avgSoil}}%; background:#34D399;"></div></div>
        </div>
      `).join('');

      document.getElementById('af-chart-water').innerHTML = agg.map(item => `
