PY := python3
OUT := output
OUT_EN := output/en

.PHONY: all all-en clean clean-en clean-all \
        fig1 fig2 fig3 fig4 fig5 fig6 \
        fig1-en fig2-en fig3-en fig4-en fig5-en fig6-en

# ---------- Chinese (default) ----------

all: fig1 fig2 fig3 fig4 fig5 fig6

fig1:
	FIG_LANG=zh $(PY) src/fig1_wealth_timeline.py

fig2:
	FIG_LANG=zh $(PY) src/fig2_salary_comparison.py

fig3:
	FIG_LANG=zh $(PY) src/fig3_nobel_background.py

fig4:
	FIG_LANG=zh $(PY) src/fig4_purchasing_power.py

fig5:
	FIG_LANG=zh $(PY) src/fig5_academic_genealogy.py

fig6:
	FIG_LANG=zh $(PY) src/fig6_lost_einsteins.py

# ---------- English ----------

all-en: fig1-en fig2-en fig3-en fig4-en fig5-en fig6-en

fig1-en:
	FIG_LANG=en $(PY) src/fig1_wealth_timeline.py

fig2-en:
	FIG_LANG=en $(PY) src/fig2_salary_comparison.py

fig3-en:
	FIG_LANG=en $(PY) src/fig3_nobel_background.py

fig4-en:
	FIG_LANG=en $(PY) src/fig4_purchasing_power.py

fig5-en:
	FIG_LANG=en $(PY) src/fig5_academic_genealogy.py

fig6-en:
	FIG_LANG=en $(PY) src/fig6_lost_einsteins.py

# ---------- Cleanup ----------

clean:
	rm -f $(OUT)/*.png $(OUT)/*.svg

clean-en:
	rm -f $(OUT_EN)/*.png $(OUT_EN)/*.svg

clean-all: clean clean-en
