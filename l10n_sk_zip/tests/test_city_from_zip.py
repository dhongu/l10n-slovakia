# ©  2026 Terrabit
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo.tests import Form, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestCityFromZip(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.country = cls.env.ref("base.sk")
        cls.Partner = cls.env["res.partner"]

    def _city(self, zip_code, name):
        return self.env["res.city"].search(
            [("country_id", "=", self.country.id), ("zipcode", "=", zip_code), ("name", "=", name)]
        )

    def test_data_loaded(self):
        self.assertTrue(self.country.enforce_cities)
        city = self._city("013 12", "Turie")
        self.assertEqual(len(city), 1)
        self.assertEqual(city.state_id, self.env.ref("l10n_sk_zip.state_sk_zi"))

    def test_unique_zip(self):
        city, state = self.Partner._l10n_sk_city_from_zip("013 12")
        self.assertEqual(city, self._city("013 12", "Turie"))
        self.assertEqual(state, self.env.ref("l10n_sk_zip.state_sk_zi"))

    def test_shared_zip_gives_state(self):
        # 013 18 is shared by several localities of the same region: only the region is known
        city, state = self.Partner._l10n_sk_city_from_zip("013 18")
        self.assertFalse(city)
        self.assertEqual(state, self.env.ref("l10n_sk_zip.state_sk_zi"))
        # the city name picks the locality
        city, state = self.Partner._l10n_sk_city_from_zip("013 18", "Lietava".upper())
        self.assertEqual(city, self._city("013 18", "Lietava"))

    def test_onchange_zip(self):
        # not saved: other modules may make more fields required on the contact form
        partner_form = Form(self.Partner)
        partner_form.name = "Test Partner"
        partner_form.country_id = self.country
        partner_form.zip = "013 12"
        self.assertEqual(partner_form.city_id, self._city("013 12", "Turie"))
        self.assertEqual(partner_form.city, "Turie")
        self.assertEqual(partner_form.state_id, self.env.ref("l10n_sk_zip.state_sk_zi"))

    def test_fix_city_from_zip(self):
        partner = self.Partner.create(
            {"name": "Test Partner", "country_id": self.country.id, "city": "Turie", "zip": "013 12"}
        )
        partner.l10n_sk_fix_city_from_zip()
        self.assertRecordValues(
            partner,
            [
                {
                    "city_id": self._city("013 12", "Turie").id,
                    "city": "Turie",
                    "zip": "013 12",
                    "state_id": self.env.ref("l10n_sk_zip.state_sk_zi").id,
                }
            ],
        )

    def test_other_country_untouched(self):
        partner = self.Partner.create(
            {"name": "Ion Popescu", "country_id": self.env.ref("base.ro").id, "city": "Turie", "zip": "013 12"}
        )
        partner.l10n_sk_fix_city_from_zip()
        self.assertFalse(partner.city_id)
        self.assertFalse(partner.state_id)

    def test_relink_batch(self):
        partner = self.Partner.create(
            {"name": "Test Partner", "country_id": self.country.id, "city": "Turie", "zip": "013 12"}
        )
        last_id, count = self.Partner._l10n_sk_relink_batch(partner.id - 1)
        self.assertGreaterEqual(count, 1)
