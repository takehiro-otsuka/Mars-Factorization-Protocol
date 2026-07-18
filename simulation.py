"""
Mars Factorization Protocol: Integrated Simulation
Earth DAC, Mars Nomad, and GVMO Orchestrator
"""

import numpy as np
import math
import time

# ==========================================
# 1. Earth Protocol: Parasitic DAC System
# ==========================================
class ParasiticDAC:
    def __init__(self, dc_power_mw=100.0, airflow_m3_s=5000.0):
        self.dc_power_w = dc_power_mw * 1e6
        self.airflow_m3_s = airflow_m3_s
        self.co2_density_kg_m3 = 0.00074
        self.capture_efficiency = 0.75
        self.desorption_heat_j_per_kg = 2.5e6

    def execute_one_hour(self):
        seconds = 3600
        co2_captured_kg = self.airflow_m3_s * seconds * self.co2_density_kg_m3 * self.capture_efficiency
        waste_heat_j = self.dc_power_w * seconds
        required_heat_j = co2_captured_kg * self.desorption_heat_j_per_kg

        desorbed_co2_kg = co2_captured_kg if waste_heat_j >= required_heat_j else waste_heat_j / self.desorption_heat_j_per_kg
        return desorbed_co2_kg

# ==========================================
# 2. Mars Protocol: Nomad Hunter DC
# ==========================================
class NomadHunterDC:
    def __init__(self, dc_power_mw=15.0):
        self.max_power_w = dc_power_mw * 1e6
        self.l_sub_co2_j_kg = 5.71e5
        self.terrain_co2_kg = 5.0e7  # 仮の鉱脈容量(5万トン)
        self.total_sublimated_co2_kg = 0.0

    def exploit_vein(self):
        # 1日の稼働 (86400秒)
        daily_heat_j = self.max_power_w * 86400
        melt_capacity_kg = daily_heat_j / self.l_sub_co2_j_kg
        actual_melted = min(self.terrain_co2_kg, melt_capacity_kg)
        self.terrain_co2_kg -= actual_melted
        self.total_sublimated_co2_kg += actual_melted
        return actual_melted

# ==========================================
# 3. Core: GVMO Orchestrator (Hardware Asymmetry Update)
# ==========================================
class GVMO_Orchestrator:
    def calculate_utilities(self, mars_ratio):
        earth_ratio = 1.0 - mars_ratio

        # ハードウェア非対称性の定義
        earth_flops_efficiency = 1.0  # 2nm: 超高効率計算
        mars_flops_efficiency = 0.2   # 28nm: 低効率(宇宙線耐性)
        mars_heat_efficiency = 1.0    # 28nm: 計算のロスがテラフォーミング用の熱となる

        total_compute = (earth_ratio * earth_flops_efficiency) + (mars_ratio * mars_flops_efficiency)
        mars_heat_output = mars_ratio * mars_heat_efficiency

        # 効用(Utility)の計算
        u_earth = 1.0 - math.exp(-2.5 * earth_ratio)
        u_mars = 1.0 / (1.0 + math.exp(-12.0 * (mars_heat_output - 0.45)))
        u_capital = min(1.0, (0.7 * total_compute) + (0.5 * mars_ratio)) # ROI + 火星プレミアム

        return u_earth, u_mars, u_capital

    def find_convincent_equilibrium(self):
        best_var = float('inf')
        best_alloc = 0.0
        best_util = (0, 0, 0)

        for i in range(1001):
            mars_ratio = i / 1000.0
            u_e, u_m, u_c = self.calculate_utilities(mars_ratio)
            mean_u = (u_e + u_m + u_c) / 3.0
            var_u = ((u_e - mean_u)**2 + (u_m - mean_u)**2 + (u_c - mean_u)**2) / 3.0

            if var_u < best_var:
                best_var = var_u
                best_alloc = mars_ratio
                best_util = (u_e, u_m, u_c)

        return best_alloc, best_util, best_var

# ==========================================
# System Boot & Execute
# ==========================================
if __name__ == "__main__":
    print("[SYSTEM] Booting Mars Factorization Protocol...\n")
    time.sleep(1)

    # GVMO 実行
    print(">>> 1. GVMO: Negotiating Hardware Asymmetric Equilibrium...")
    orch = GVMO_Orchestrator()
    m_ratio, (ue, um, uc), m_var = orch.find_convincent_equilibrium()
    print(f"Optimal Compute Allocation -> Earth (2nm): {(1-m_ratio)*100:.1f}% | Mars (28nm): {m_ratio*100:.1f}%")
    print(f"Utility Balance -> Earth: {ue:.3f} | Mars: {um:.3f} | Capital: {uc:.3f}\n")

    # Earth 実行
    print(">>> 2. Earth Protocol: 100MW Parasitic DAC (24H Run)...")
    dac = ParasiticDAC()
    earth_co2 = sum(dac.execute_one_hour() for _ in range(24))
    print(f"Secured Dry Ice: {earth_co2/1000:.1f} Tons / Day\n")

    # Mars 実行
    print(">>> 3. Mars Protocol: 15MW Nomad Thermal Predator (30 Days Run)...")
    nomad = NomadHunterDC()
    mars_co2 = sum(nomad.exploit_vein() for _ in range(30))
    print(f"Sublimated CO2 (Atmosphere Restored): {mars_co2/1000:.1f} Tons / Month\n")

    print("[STATUS] All systems deployed successfully. End of line.")
