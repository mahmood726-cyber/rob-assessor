"""
RoB Assessor — Risk of Bias Assessment Tool
Selenium Test Suite: 25 tests covering RoB 2, ROBINS-I, assessment workflow, summary, and export.
Run: python test_rob_assessor.py
"""
import sys, os, time, io, unittest
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rob-assessor.html')
URL = 'file:///' + HTML_PATH.replace('\\', '/')


def get_driver():
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--window-size=1400,900')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    driver = webdriver.Chrome(options=opts)
    driver.implicitly_wait(2)
    return driver


class RoBAssessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.driver.get(URL)
        # Clear any stored data
        cls.driver.execute_script("try{localStorage.removeItem('robassessor-data')}catch(e){}")
        cls.driver.get(URL)
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        logs = cls.driver.get_log('browser')
        severe = [l for l in logs if l['level'] == 'SEVERE' and 'favicon' not in l.get('message', '')]
        if severe:
            print(f"\nJS ERRORS ({len(severe)}):")
            for l in severe:
                print(f"  {l['message']}")
        cls.driver.quit()

    def _reload(self):
        self.driver.execute_script("try{localStorage.removeItem('robassessor-data')}catch(e){}")
        self.driver.get(URL)
        time.sleep(0.3)

    def _click(self, by, val):
        el = WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((by, val)))
        self.driver.execute_script("arguments[0].click()", el)
        return el

    def _add_study(self, name, framework='rob2'):
        self.driver.find_element(By.ID, 'studyId').clear()
        self.driver.find_element(By.ID, 'studyId').send_keys(name)
        sel = self.driver.find_element(By.ID, 'framework')
        for opt in sel.find_elements(By.TAG_NAME, 'option'):
            if opt.get_attribute('value') == framework:
                opt.click()
                break
        self._click(By.ID, 'addStudyBtn')
        time.sleep(0.2)

    # ─── 1. PAGE LOAD ───
    def test_01_page_loads(self):
        """Page loads with correct title."""
        self.assertIn('RoB Assessor', self.driver.title)

    def test_02_hero_visible(self):
        """Hero header is visible."""
        hero = self.driver.find_element(By.CSS_SELECTOR, '.hero-title')
        self.assertIn('RoB Assessor', hero.text)

    def test_03_four_tabs(self):
        """All 4 tabs exist."""
        tabs = self.driver.find_elements(By.CSS_SELECTOR, '.tab-btn')
        self.assertEqual(len(tabs), 4)

    def test_04_empty_state(self):
        """Shows empty state message when no studies."""
        self._reload()
        empty = self.driver.find_element(By.ID, 'emptyStudies')
        self.assertTrue(empty.is_displayed())

    # ─── 2. ADD STUDIES ───
    def test_05_add_rob2_study(self):
        """Adding a RoB 2 study shows it in the list."""
        self._reload()
        self._add_study('Smith 2020', 'rob2')
        items = self.driver.find_elements(By.CSS_SELECTOR, '.study-item')
        self.assertEqual(len(items), 1)
        self.assertIn('Smith 2020', items[0].text)
        self.assertIn('RoB 2', items[0].text)

    def test_06_add_robins_study(self):
        """Adding a ROBINS-I study shows the correct framework badge."""
        self._reload()
        self._add_study('Jones 2021', 'robins-i')
        items = self.driver.find_elements(By.CSS_SELECTOR, '.study-item')
        self.assertEqual(len(items), 1)
        self.assertIn('ROBINS-I', items[0].text)

    def test_07_duplicate_rejected(self):
        """Duplicate study names are rejected."""
        self._reload()
        self._add_study('Smith 2020', 'rob2')
        # Try to add again — should alert
        self.driver.find_element(By.ID, 'studyId').clear()
        self.driver.find_element(By.ID, 'studyId').send_keys('Smith 2020')
        self._click(By.ID, 'addStudyBtn')
        time.sleep(0.3)
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
        except Exception:
            pass
        items = self.driver.find_elements(By.CSS_SELECTOR, '.study-item')
        self.assertEqual(len(items), 1)

    def test_08_csv_import(self):
        """CSV import adds multiple studies."""
        self._reload()
        csv_data = "CRASH 2004, rob2\nNICE-SUGAR 2009, rob2\nObserv 2015, robins-i"
        textarea = self.driver.find_element(By.ID, 'csvImport')
        textarea.send_keys(csv_data)
        self._click(By.ID, 'importCsvBtn')
        time.sleep(0.3)
        items = self.driver.find_elements(By.CSS_SELECTOR, '.study-item')
        self.assertEqual(len(items), 3)

    def test_09_delete_study(self):
        """Deleting a study removes it from the list."""
        self._reload()
        self._add_study('ToDelete', 'rob2')
        self.assertEqual(len(self.driver.find_elements(By.CSS_SELECTOR, '.study-item')), 1)
        del_btn = self.driver.find_element(By.CSS_SELECTOR, '[data-delidx="0"]')
        self.driver.execute_script("arguments[0].click()", del_btn)
        time.sleep(0.2)
        self.assertEqual(len(self.driver.find_elements(By.CSS_SELECTOR, '.study-item')), 0)

    # ─── 3. TAB NAVIGATION ───
    def test_10_tab_navigation(self):
        """Clicking tabs switches panels."""
        self._click(By.ID, 'tab-summary')
        time.sleep(0.2)
        panel = self.driver.find_element(By.ID, 'panel-summary')
        self.assertIn('active', panel.get_attribute('class'))
        self._click(By.ID, 'tab-studies')

    def test_11_keyboard_tab_navigation(self):
        """Arrow keys navigate tabs."""
        self._reload()
        tab = self.driver.find_element(By.ID, 'tab-studies')
        tab.send_keys(Keys.ARROW_RIGHT)
        time.sleep(0.2)
        assess_tab = self.driver.find_element(By.ID, 'tab-assess')
        self.assertEqual(assess_tab.get_attribute('aria-selected'), 'true')

    # ─── 4. DARK MODE ───
    def test_12_dark_mode(self):
        """Dark mode toggle works."""
        self._reload()
        btn = self.driver.find_element(By.ID, 'themeToggle')
        self.driver.execute_script("arguments[0].click()", btn)
        time.sleep(0.2)
        theme = self.driver.find_element(By.TAG_NAME, 'html').get_attribute('data-theme')
        self.assertEqual(theme, 'dark')
        self.driver.execute_script("arguments[0].click()", btn)

    # ─── 5. ASSESSMENT WORKFLOW (RoB 2) ───
    def test_13_assess_panel_opens(self):
        """Clicking a study opens the assessment panel."""
        self._reload()
        self._add_study('Test RCT', 'rob2')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        content = self.driver.find_element(By.ID, 'assessContent')
        self.assertTrue(content.is_displayed())

    def test_14_rob2_five_domains(self):
        """RoB 2 shows 5 domain navigation items."""
        self._reload()
        self._add_study('Test RCT', 'rob2')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        domains = self.driver.find_elements(By.CSS_SELECTOR, '#domainNav .domain-item')
        self.assertEqual(len(domains), 5)

    def test_15_rob2_signaling_questions(self):
        """Domain 1 shows signaling questions with response options."""
        self._reload()
        self._add_study('Test RCT', 'rob2')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        questions = self.driver.find_elements(By.CSS_SELECTOR, '.sq-question')
        self.assertEqual(len(questions), 3)  # D1 has 3 questions
        opts = self.driver.find_elements(By.CSS_SELECTOR, '.sq-opt')
        self.assertGreater(len(opts), 0)

    def test_16_answer_signaling_question(self):
        """Clicking a signaling question option selects it."""
        self._reload()
        self._add_study('Test RCT', 'rob2')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        # Click "Yes" for first question
        opts = self.driver.find_elements(By.CSS_SELECTOR, '.sq-opt')
        self.driver.execute_script("arguments[0].click()", opts[0])
        time.sleep(0.2)
        # Verify it's selected
        opts = self.driver.find_elements(By.CSS_SELECTOR, '.sq-opt')
        self.assertIn('selected', opts[0].get_attribute('class'))

    def test_17_set_domain_judgment(self):
        """Setting a domain judgment updates the navigation."""
        self._reload()
        self._add_study('Test RCT', 'rob2')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        # Click "Low" judgment
        j_opts = self.driver.find_elements(By.CSS_SELECTOR, '.j-opt')
        self.driver.execute_script("arguments[0].click()", j_opts[0])  # "Low"
        time.sleep(0.3)
        # Domain nav should show green
        first_domain = self.driver.find_element(By.CSS_SELECTOR, '#domainNav .domain-item')
        self.assertIn('judgment-low', first_domain.get_attribute('class'))

    def test_18_navigate_domains(self):
        """Clicking domain 2 switches the question set."""
        self._reload()
        self._add_study('Test RCT', 'rob2')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        domains = self.driver.find_elements(By.CSS_SELECTOR, '#domainNav .domain-item')
        self.driver.execute_script("arguments[0].click()", domains[1])
        time.sleep(0.3)
        title = self.driver.find_element(By.ID, 'domainTitle').text
        self.assertIn('Deviations', title)

    # ─── 6. ROBINS-I ASSESSMENT ───
    def test_19_robins_seven_domains(self):
        """ROBINS-I shows 7 domain navigation items."""
        self._reload()
        self._add_study('Observ 2021', 'robins-i')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        domains = self.driver.find_elements(By.CSS_SELECTOR, '#domainNav .domain-item')
        self.assertEqual(len(domains), 7)

    def test_20_robins_judgment_options(self):
        """ROBINS-I has 5 judgment options (Low, Moderate, Serious, Critical, NI)."""
        self._reload()
        self._add_study('Observ 2021', 'robins-i')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        j_opts = self.driver.find_elements(By.CSS_SELECTOR, '.j-opt')
        self.assertEqual(len(j_opts), 5)
        labels = [o.text for o in j_opts]
        self.assertIn('Critical', labels)
        self.assertIn('No information', labels)

    # ─── 7. OVERALL JUDGMENT ───
    def test_21_overall_computed(self):
        """Completing all domains computes overall judgment."""
        self._reload()
        self._add_study('Full RCT', 'rob2')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        # Set all 5 domains to "Low"
        for d in range(5):
            domains = self.driver.find_elements(By.CSS_SELECTOR, '#domainNav .domain-item')
            self.driver.execute_script("arguments[0].click()", domains[d])
            time.sleep(0.2)
            j_opts = self.driver.find_elements(By.CSS_SELECTOR, '.j-opt')
            self.driver.execute_script("arguments[0].click()", j_opts[0])  # "Low"
            time.sleep(0.2)
        overall = self.driver.find_element(By.ID, 'overallJudgment').text
        self.assertEqual(overall, 'Low')

    def test_22_overall_worst_domain(self):
        """Overall = worst domain judgment."""
        self._reload()
        self._add_study('Mixed RCT', 'rob2')
        item = self.driver.find_element(By.CSS_SELECTOR, '.study-item')
        self.driver.execute_script("arguments[0].click()", item)
        time.sleep(0.3)
        # Set 4 domains to "Low", 1 to "High"
        for d in range(5):
            domains = self.driver.find_elements(By.CSS_SELECTOR, '#domainNav .domain-item')
            self.driver.execute_script("arguments[0].click()", domains[d])
            time.sleep(0.2)
            j_opts = self.driver.find_elements(By.CSS_SELECTOR, '.j-opt')
            idx = 2 if d == 3 else 0  # D4 = "High", rest = "Low"
            self.driver.execute_script("arguments[0].click()", j_opts[idx])
            time.sleep(0.2)
        overall = self.driver.find_element(By.ID, 'overallJudgment').text
        self.assertEqual(overall, 'High')

    # ─── 8. SUMMARY TAB ───
    def test_23_traffic_light_table(self):
        """Summary tab shows traffic light table."""
        self._reload()
        self._add_study('Study A', 'rob2')
        self._add_study('Study B', 'rob2')
        self._click(By.ID, 'tab-summary')
        time.sleep(0.3)
        content = self.driver.find_element(By.ID, 'summaryContent')
        self.assertTrue(content.is_displayed())
        dots = self.driver.find_elements(By.CSS_SELECTOR, '.tl-dot')
        # 2 studies x (5 domains + 1 overall) = 12 dots
        self.assertEqual(len(dots), 12)

    def test_24_bar_chart(self):
        """Summary tab shows domain bar chart."""
        # Continuing from previous test state
        chart = self.driver.find_element(By.ID, 'barChart')
        bars = chart.find_elements(By.CSS_SELECTOR, '.bar-row')
        self.assertGreater(len(bars), 0)

    # ─── 9. EXPORT ───
    def test_25_export_buttons_present(self):
        """Export tab has all 4 export options."""
        self._click(By.ID, 'tab-export')
        time.sleep(0.2)
        csv_btn = self.driver.find_element(By.ID, 'exportCsvBtn')
        json_btn = self.driver.find_element(By.ID, 'exportJsonBtn')
        methods_btn = self.driver.find_element(By.ID, 'exportMethodsBtn')
        print_btn = self.driver.find_element(By.ID, 'printBtn')
        self.assertTrue(csv_btn.is_displayed())
        self.assertTrue(json_btn.is_displayed())
        self.assertTrue(methods_btn.is_displayed())
        self.assertTrue(print_btn.is_displayed())


if __name__ == '__main__':
    unittest.main(verbosity=2)
