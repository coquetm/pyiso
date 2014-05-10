from pyiso import client_factory
from unittest import TestCase
import logging
import StringIO
import pandas as pd
import pytz
from datetime import date, datetime, timedelta
from bs4 import BeautifulSoup


class TestCAISOBase(TestCase):
    def setUp(self):
        self.ren_report_tsv = StringIO.StringIO("03/12/14\t\t\tHourly Breakdown of Renewable Resources (MW)\t\t\t\t\t\t\t\t\t\t\t\t\n\
\tHour\t\tGEOTHERMAL\tBIOMASS\t\tBIOGAS\t\tSMALL HYDRO\tWIND TOTAL\tSOLAR PV\tSOLAR THERMAL\t\t\t\t\n\
\t1\t\t900\t\t313\t\t190\t\t170\t\t1596\t\t0\t\t0\n\
\t2\t\t900\t\t314\t\t189\t\t169\t\t1814\t\t0\t\t0\n\
\t3\t\t900\t\t328\t\t190\t\t170\t\t2076\t\t0\t\t0\n\
\t4\t\t900\t\t334\t\t190\t\t167\t\t2086\t\t0\t\t0\n\
\t5\t\t900\t\t344\t\t190\t\t167\t\t1893\t\t0\t\t0\n\
\t6\t\t900\t\t344\t\t190\t\t166\t\t1650\t\t0\t\t0\n\
\t7\t\t899\t\t339\t\t189\t\t177\t\t1459\t\t0\t\t0\n\
\t8\t\t897\t\t341\t\t188\t\t179\t\t1487\t\t245\t\t0\n\
\t9\t\t898\t\t341\t\t187\t\t171\t\t1502\t\t1455\t\t5\n\
\t10\t\t898\t\t341\t\t186\t\t169\t\t1745\t\t2613\t\t251\n\
\t11\t\t898\t\t342\t\t183\t\t168\t\t2204\t\t3318\t\t336\n\
\t12\t\t897\t\t358\t\t185\t\t168\t\t2241\t\t3558\t\t341\n\
\t13\t\t897\t\t367\t\t189\t\t169\t\t1850\t\t3585\t\t326\n\
\t14\t\t897\t\t367\t\t191\t\t169\t\t1632\t\t3598\t\t316\n\
\t15\t\t892\t\t364\t\t193\t\t171\t\t1317\t\t3541\t\t299\n\
\t16\t\t890\t\t368\t\t192\t\t174\t\t1156\t\t3359\t\t338\n\
\t17\t\t891\t\t367\t\t189\t\t187\t\t1082\t\t2697\t\t400\n\
\t18\t\t892\t\t362\t\t192\t\t202\t\t1047\t\t1625\t\t325\n\
\t19\t\t892\t\t361\t\t196\t\t205\t\t861\t\t306\t\t32\n\
\t20\t\t892\t\t359\t\t197\t\t214\t\t725\t\t0\t\t0\n\
\t21\t\t895\t\t354\t\t192\t\t208\t\t722\t\t0\t\t0\n\
\t22\t\t900\t\t355\t\t182\t\t209\t\t689\t\t0\t\t0\n\
\t23\t\t901\t\t355\t\t182\t\t198\t\t482\t\t0\t\t0\n\
\t24\t\t902\t\t357\t\t183\t\t170\t\t507\t\t0\t\t0\n\
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\
\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\n\
\t\t\tHourly Breakdown of Total Production by Resource Type (MW)\t\t\t\t\t\t\t\t\t\t\t\t\n\
\tHour\t\tRENEWABLES\tNUCLEAR\t\tTHERMAL\t\tIMPORTS\t\tHYDRO\t\t\t\t\t\n\
\t1\t\t3170\t\t1092\t\t6862\t\t9392\t\t871\t\t\t\t\n\
\t2\t\t3386\t\t1092\t\t6181\t\t9144\t\t709\t\t\t\t\n\
\t3\t\t3663\t\t1092\t\t6016\t\t8993\t\t675\t\t\t\t\n\
\t4\t\t3678\t\t1091\t\t5900\t\t9107\t\t669\t\t\t\t\n\
\t5\t\t3494\t\t1092\t\t6041\t\t9080\t\t840\t\t\t\t\n\
\t6\t\t3251\t\t1091\t\t7115\t\t8848\t\t919\t\t\t\t\n\
\t7\t\t3064\t\t1091\t\t9917\t\t8464\t\t1269\t\t\t\t\n\
\t8\t\t3337\t\t1091\t\t10955\t\t8694\t\t1387\t\t\t\t\n\
\t9\t\t4559\t\t1091\t\t10291\t\t8667\t\t1120\t\t\t\t\n\
\t10\t\t6204\t\t1091\t\t8967\t\t8783\t\t829\t\t\t\t\n\
\t11\t\t7449\t\t1091\t\t8095\t\t8776\t\t656\t\t\t\t\n\
\t12\t\t7747\t\t1089\t\t8068\t\t8565\t\t703\t\t\t\t\n\
\t13\t\t7382\t\t1087\t\t8157\t\t8736\t\t862\t\t\t\t\n\
\t14\t\t7171\t\t1085\t\t8564\t\t8633\t\t973\t\t\t\t\n\
\t15\t\t6776\t\t1079\t\t8588\t\t8832\t\t1004\t\t\t\t\n\
\t16\t\t6477\t\t1079\t\t8890\t\t8857\t\t980\t\t\t\t\n\
\t17\t\t5812\t\t1080\t\t8937\t\t9168\t\t1210\t\t\t\t\n\
\t18\t\t4645\t\t1081\t\t9620\t\t9481\t\t1443\t\t\t\t\n\
\t19\t\t2853\t\t1081\t\t11258\t\t9653\t\t1763\t\t\t\t\n\
\t20\t\t2388\t\t1081\t\t12971\t\t10022\t\t1979\t\t\t\t\n\
\t21\t\t2370\t\t1081\t\t12644\t\t10324\t\t2130\t\t\t\t\n\
\t22\t\t2335\t\t1082\t\t11820\t\t10069\t\t1774\t\t\t\t\n\
\t23\t\t2119\t\t1085\t\t10712\t\t9871\t\t1250\t\t\t\t\n\
\t24\t\t2118\t\t1082\t\t9800\t\t8904\t\t935\t\t\t\t\n\
")

        self.sld_fcst_xml = StringIO.StringIO("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n\
<OASISReport xmlns=\"http://www.caiso.com/soa/OASISReport_v1.xsd\">\n\
<MessageHeader>\n\
<TimeDate>2014-05-09T17:50:06-00:00</TimeDate>\n\
<Source>OASIS</Source>\n\
<Version>v20140401</Version>\n\
</MessageHeader>\n\
<MessagePayload>\n\
<RTO>\n\
<name>CAISO</name>\n\
<REPORT_ITEM>\n\
<REPORT_HEADER>\n\
<SYSTEM>OASIS</SYSTEM>\n\
<TZ>PPT</TZ>\n\
<REPORT>SLD_FCST</REPORT>\n\
<MKT_TYPE>RTM</MKT_TYPE>\n\
<EXECUTION_TYPE>RTPD</EXECUTION_TYPE>\n\
<UOM>MW</UOM>\n\
<INTERVAL>ENDING</INTERVAL>\n\
<SEC_PER_INTERVAL>900</SEC_PER_INTERVAL>\n\
</REPORT_HEADER>\n\
<REPORT_DATA>\n\
<DATA_ITEM>SYS_FCST_15MIN_MW</DATA_ITEM>\n\
<RESOURCE_NAME>CA ISO-TAC</RESOURCE_NAME>\n\
<OPR_DATE>2014-05-08</OPR_DATE>\n\
<INTERVAL_NUM>50</INTERVAL_NUM>\n\
<INTERVAL_START_GMT>2014-05-08T19:15:00-00:00</INTERVAL_START_GMT>\n\
<INTERVAL_END_GMT>2014-05-08T19:30:00-00:00</INTERVAL_END_GMT>\n\
<VALUE>26723</VALUE>\n\
</REPORT_DATA>\n\
<REPORT_DATA>\n\
<DATA_ITEM>SYS_FCST_5MIN_MW</DATA_ITEM>\n\
<RESOURCE_NAME>CA ISO-TAC</RESOURCE_NAME>\n\
<OPR_DATE>2014-05-08</OPR_DATE>\n\
<INTERVAL_NUM>144</INTERVAL_NUM>\n\
<INTERVAL_START_GMT>2014-05-08T18:55:00-00:00</INTERVAL_START_GMT>\n\
<INTERVAL_END_GMT>2014-05-08T19:00:00-00:00</INTERVAL_END_GMT>\n\
<VALUE>26755</VALUE>\n\
</REPORT_DATA>\n\
<REPORT_DATA>\n\
<DATA_ITEM>SYS_FCST_5MIN_MW</DATA_ITEM>\n\
<RESOURCE_NAME>PGE-TAC</RESOURCE_NAME>\n\
<OPR_DATE>2014-05-08</OPR_DATE>\n\
<INTERVAL_NUM>146</INTERVAL_NUM>\n\
<INTERVAL_START_GMT>2014-05-08T19:05:00-00:00</INTERVAL_START_GMT>\n\
<INTERVAL_END_GMT>2014-05-08T19:10:00-00:00</INTERVAL_END_GMT>\n\
<VALUE>11530</VALUE>\n\
</REPORT_DATA>\n\
</REPORT_ITEM>\n\
<DISCLAIMER_ITEM>\n\
<DISCLAIMER>The contents of these pages are subject to change without notice.  Decisions based on information contained within the California ISO's web site are the visitor's sole responsibility.</DISCLAIMER>\n\
</DISCLAIMER_ITEM>\n\
</RTO>\n\
</MessagePayload>\n\
</OASISReport>")

        self.todays_outlook_renewables = StringIO.StringIO("<!doctype html public \"-//W3C//DTD HTML 3.2 Final//EN\">\n\
\n\
<HTML>\n\
<HEAD>\n\
<meta http-equiv=\"refresh\" content=\"600\">\n\
<TITLE>System Conditions - The California ISO</TITLE>\n\
<LINK REL=\"stylesheet\" TYPE=\"text/css\" HREF=\"/styles01.css\">\n\
<LINK REL=\"stylesheet\" TYPE=\"text/css\" HREF=\"http://www.caiso.com/Style%20Library/caiso/css/outlook.css\">\n\
<meta http-equiv=\"refresh\" content=\"300\">\n\
</HEAD>\n\
\n\
<BODY BGCOLOR=\"#ffffff\" TEXT=\"#000000\" LINK=\"#d96100\" VLINK=\"#666666\" TOPMARGIN=\"0\">\n\
<table width=\"100%\" border=\"0\" cellspacing=\"0\" cellpadding=\"0\">\n\
<tr>\n\
  <td valign=\"top\"><p><span class=\"to_callout1\">Current Renewables</span><br />\n\
    <span class=\"to_readings\" id=\"totalrenewables\">\n\
      6086 \n\
      MW</span><br />\n\
  </p>\n\
    <p><br />\n\
      <a href=\"http://www.caiso.com/market/Pages/ReportsBulletins/DailyRenewablesWatch.aspx\" target=\"_top\"><img src=\"http://www.caiso.com/PublishingImages/Today's%20Outlook%20Images/RenewablesWatchLogo.jpg\" width=\"150\" height=\"57\" alt=\"Renewables Watch\" border=\"0\"></a><br />\n\
      <span class=\"to_callout2\">The Renewables Watch provides actual renewable energy production within the ISO Grid.</span><br />\n\
    <a href=\"/green/renewrpt/DailyRenewablesWatch.pdf\" target=\"_blank\"><span class=\"to_about\">Click here to view yesterday's output.</span></a></p></td>\n\
  <td class=\"docdate\" valign=\"top\" align=\"right\"><img src=\"/outlook/SP/ems_renewables.gif\"><br /> <br /><img src=\"http://www.caiso.com/PublishingImages/RenewablesGraphKey.gif\"></td>\n\
</tr>  </table>\n\
</BODY>\n\
</HTML>\n\
\n\
")

    def create_client(self, ba_name):
        # set up client with logging
        c = client_factory(ba_name)
        handler = logging.StreamHandler()
        c.logger.addHandler(handler)
        c.logger.setLevel(logging.DEBUG)
        return c

    def test_request_renewable_report(self):
        c = self.create_client('CAISO')
        response = c.request('http://content.caiso.com/green/renewrpt/20140312_DailyRenewablesWatch.txt')
        self.assertIn('Hourly Breakdown of Renewable Resources (MW)', response.text)

    def test_parse_ren_report_both(self):
        c = self.create_client('CAISO')

        # top half
        top_df = c.parse_to_df(self.ren_report_tsv,
                            skiprows=1, nrows=24, header=1,
                            delimiter='\t+')
        self.assertEqual(list(top_df.columns), ['Hour', 'GEOTHERMAL', 'BIOMASS', 'BIOGAS', 'SMALL HYDRO', 'WIND TOTAL', 'SOLAR PV', 'SOLAR THERMAL'])
        self.assertEqual(len(top_df), 24)

        # bottom half
        bot_df = c.parse_to_df(self.ren_report_tsv,
                            skiprows=3, nrows=24, header=3,
                            delimiter='\t+')
        self.assertEqual(list(bot_df.columns), ['Hour', 'RENEWABLES', 'NUCLEAR', 'THERMAL', 'IMPORTS', 'HYDRO'])
        self.assertEqual(len(bot_df), 24)

    def test_parse_ren_report_bot(self):
        c = self.create_client('CAISO')

        # bottom half
        bot_df = c.parse_to_df(self.ren_report_tsv,
                            skiprows=29, nrows=24, header=29,
                            delimiter='\t+')
        self.assertEqual(list(bot_df.columns), ['Hour', 'RENEWABLES', 'NUCLEAR', 'THERMAL', 'IMPORTS', 'HYDRO'])
        self.assertEqual(len(bot_df), 24)

    def test_dt_index(self):
        c = self.create_client('CAISO')
        df = c.parse_to_df(self.ren_report_tsv,
                            skiprows=1, nrows=24, header=1,
                            delimiter='\t+')
        indexed = c.set_dt_index(df, date(2014, 3, 12), df['Hour'])
        self.assertEqual(type(indexed.index), pd.tseries.index.DatetimeIndex)
        self.assertEqual(indexed.index[0].hour, 7)

    def test_pivot(self):
        c = self.create_client('CAISO')
        df = c.parse_to_df(self.ren_report_tsv,
                            skiprows=1, nrows=24, header=1,
                            delimiter='\t+')
        indexed = c.set_dt_index(df, date(2014, 3, 12), df['Hour'])
        indexed.pop('Hour')
        pivoted = c.unpivot(indexed)

        # no rows with 'Hour'
        hour_rows = pivoted[pivoted['level_1']=='Hour']
        self.assertEqual(len(hour_rows), 0)

        # number of rows is from number of columns
        self.assertEqual(len(pivoted), 24*len(indexed.columns))

    def test_fetch_oasis_demand_forecast(self):
        c = self.create_client('CAISO')
        ts = c.utcify('2014-05-08 12:00')
        payload = {'queryname': 'SLD_FCST',
                   'market_run_id': 'RTM',
                   'startdatetime': (ts-timedelta(minutes=20)).strftime(c.oasis_request_time_format),
                   'enddatetime': (ts+timedelta(minutes=20)).strftime(c.oasis_request_time_format),
                  }
        payload.update(c.base_payload)
        data = c.fetch_oasis(payload=payload)
        self.assertEqual(len(data), 55)
        self.assertEqual(str(data[0]), '<report_data>\n\
<data_item>SYS_FCST_15MIN_MW</data_item>\n\
<resource_name>CA ISO-TAC</resource_name>\n\
<opr_date>2014-05-08</opr_date>\n\
<interval_num>50</interval_num>\n\
<interval_start_gmt>2014-05-08T19:15:00-00:00</interval_start_gmt>\n\
<interval_end_gmt>2014-05-08T19:30:00-00:00</interval_end_gmt>\n\
<value>26723</value>\n\
</report_data>')

    def test_parse_oasis_demand_forecast(self):
        # set up list of data
        c = self.create_client('CAISO')
        soup = BeautifulSoup(self.sld_fcst_xml)
        data = soup.find_all('report_data')

        # parse
        parsed_data = c.parse_oasis_demand_forecast(data)

        # test
        self.assertEqual(len(parsed_data), 1)
        expected = {'ba_name': 'CAISO', 
                    'timestamp': datetime(2014, 5, 8, 18, 55, tzinfo=pytz.utc),
                    'freq': '5m', 'market': 'RT5M',
                    'load_MW': 26755.0}
        self.assertEqual(expected, parsed_data[0])

    def test_parse_todays_outlook_renwables(self):
        # set up soup and ts
        c = self.create_client('CAISO')
        soup = BeautifulSoup(self.todays_outlook_renewables)
        ts = c.utcify('2014-05-08 12:00')

        # parse
        parsed_data = c.parse_todays_outlook_renewables(soup, ts)

        # test
        expected = [{'ba_name': 'CAISO',
                      'freq': '10m',
                      'fuel_name': 'renewable',
                      'gen_MW': 6086.0,
                      'market': 'RT5M',
                      'timestamp': datetime(2014, 5, 8, 19, 0, tzinfo=pytz.utc)}]
        self.assertEqual(parsed_data, expected)
