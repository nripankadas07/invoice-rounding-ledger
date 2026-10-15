import copy,json,unittest
from pathlib import Path
import invoice_rounding_ledger as m

class Behavior(unittest.TestCase):
    def setUp(self):
        self.d=json.loads((Path(__file__).parent/'example.json').read_text())
    def bad(self):
        with self.assertRaises(m.InputError):m.analyze(self.d)
    def test_unknown_field_rejected(self):
        self.d['unknown']=True;self.bad()

    def test_half_minor_unit_allocation(self):
        r=m.analyze(self.d);self.assertEqual(r['allocated_tax_minor'],2);self.assertEqual([x['allocated_tax_minor'] for x in r['lines']],[1,1,0]);self.assertEqual(r['tax_groups'][0]['difference_minor'],-1)
    def test_ties_away_from_zero(self):
        from fractions import Fraction
        self.assertEqual(m.half_up(Fraction(-3,2)),-2);self.assertEqual(m.half_up(Fraction(3,2)),2)
    def test_negative_credit_allocations_sum(self):
        for x in self.d['lines']:x['quantity']='-1'
        r=m.analyze(self.d);self.assertEqual(r['allocated_tax_minor'],-2);self.assertEqual(sum(x['allocated_tax_minor'] for x in r['lines']),-2)
    def test_canonical_rate_groups(self):
        self.d['lines'][0]['tax_rate']='0.050';self.assertEqual(len(m.analyze(self.d)['tax_groups']),1)
    def test_permutation_invariant(self):
        r=m.analyze(self.d);self.d['lines'].reverse();self.assertEqual(m.analyze(self.d),r)
    def test_independent_rate_groups(self):
        self.d['lines'][0]['tax_rate']='0.10';r=m.analyze(self.d);self.assertEqual(len(r['tax_groups']),2);self.assertEqual(r['allocated_tax_minor'],2)
    def test_discount_and_fractional_quantity(self):
        self.d['lines']=[dict(self.d['lines'][0],quantity='2.5',unit_price='10',discount='0.2',tax_rate='0.05')];r=m.analyze(self.d);self.assertEqual(r['payable_using_line_net_minor'],2100)
    def test_net_rounding_difference(self):
        for x in self.d['lines']:x.update(unit_price='0.005',tax_rate='0')
        self.assertEqual(m.analyze(self.d)['net_rounding_difference_minor'],-1)
    def test_mixed_sign_conservation(self):
        self.d['lines'][0]['quantity']='-1';r=m.analyze(self.d);self.assertEqual(sum(x['allocated_tax_minor'] for x in r['lines']),r['allocated_tax_minor'])
    def test_float_money_rejected(self):
        self.d['lines'][0]['unit_price']=0.1;self.bad()
    def test_exponent_money_rejected(self):
        self.d['lines'][0]['unit_price']='1e2';self.bad()
    def test_duplicate_id_rejected(self):
        self.d['lines'][1]['id']='A';self.bad()
    def test_bad_discount(self):
        self.d['lines'][0]['discount']='1.1';self.bad()
    def test_negative_price(self):
        self.d['lines'][0]['unit_price']='-1';self.bad()

if __name__ == '__main__':unittest.main()
