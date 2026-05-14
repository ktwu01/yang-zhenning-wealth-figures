PY := python3
OUT := output

.PHONY: all clean fig1 fig2 fig3 fig4 fig5 fig6

all: fig1 fig2 fig3 fig4 fig5 fig6

fig1:
	$(PY) src/fig1_wealth_timeline.py

fig2:
	$(PY) src/fig2_salary_comparison.py

fig3:
	$(PY) src/fig3_nobel_background.py

fig4:
	$(PY) src/fig4_purchasing_power.py

fig5:
	$(PY) src/fig5_academic_genealogy.py

fig6:
	$(PY) src/fig6_lost_einsteins.py

clean:
	rm -f $(OUT)/*.png $(OUT)/*.svg
