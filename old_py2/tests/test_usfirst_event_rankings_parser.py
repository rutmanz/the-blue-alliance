import unittest2

from datafeeds.usfirst_event_rankings_parser import UsfirstEventRankingsParser


@unittest2.skip
class TestUsfirstEventRankingsParser(unittest2.TestCase):
    def test_parse_2012ct(self):
        with open('test_data/usfirst_html/usfirst_event_rankings_2012ct.html', 'r') as f:
            rankings, _ = UsfirstEventRankingsParser.parse(f.read())

        self.assertEqual(rankings, [['Rank', 'Team', 'QS', 'HP', 'BP', 'TP', 'CP', 'Record (W-L-T)', 'DQ', 'Played'], ['1', '2168', '32.00', '147.00', '60.00', '208.00', '14', '9-1-0', '0', '10'], ['2', '118', '31.00', '168.00', '90.00', '231.00', '17', '7-3-0', '0', '10'], ['3', '177', '30.00', '177.00', '120.00', '151.00', '14', '8-2-0', '0', '10'], ['4', '195', '29.00', '116.00', '70.00', '190.00', '16', '6-3-1', '0', '10'], ['5', '237', '28.00', '120.00', '60.00', '123.00', '14', '7-3-0', '0', '10'], ['6', '1071', '28.00', '115.00', '120.00', '142.00', '10', '9-1-0', '0', '10'], ['7', '173', '28.00', '114.00', '110.00', '108.00', '14', '7-3-0', '0', '10'], ['8', '1073', '28.00', '110.00', '100.00', '152.00', '11', '8-1-1', '0', '10'], ['9', '694', '28.00', '78.00', '100.00', '140.00', '14', '7-3-0', '0', '10'], ['10', '558', '27.00', '152.00', '100.00', '145.00', '13', '7-3-0', '0', '10'], ['11', '175', '27.00', '141.00', '160.00', '117.00', '13', '7-3-0', '0', '10'], ['12', '181', '26.00', '151.00', '70.00', '95.00', '14', '6-4-0', '0', '10'], ['13', '176', '26.00', '120.00', '60.00', '90.00', '18', '4-6-0', '0', '10'], ['14', '1511', '26.00', '111.00', '80.00', '164.00', '14', '6-4-0', '0', '10'], ['15', '126', '26.00', '108.00', '70.00', '165.00', '14', '6-4-0', '0', '10'], ['16', '4122', '26.00', '92.00', '100.00', '78.00', '14', '6-4-0', '0', '10'], ['17', '869', '25.00', '68.00', '130.00', '75.00', '12', '6-3-1', '0', '10'], ['18', '3464', '24.00', '135.00', '80.00', '109.00', '14', '5-5-0', '0', '10'], ['19', '3467', '24.00', '101.00', '80.00', '123.00', '10', '7-3-0', '0', '10'], ['20', '3718', '24.00', '100.00', '60.00', '106.00', '12', '6-4-0', '0', '10'], ['21', '3461', '24.00', '79.00', '30.00', '94.00', '14', '5-5-0', '0', '10'], ['22', '4055', '24.00', '78.00', '80.00', '79.00', '16', '4-6-0', '0', '10'], ['23', '1922', '23.00', '114.00', '110.00', '151.00', '10', '6-3-1', '0', '10'], ['24', '95', '22.00', '120.00', '70.00', '123.00', '14', '4-6-0', '0', '10'], ['25', '1991', '22.00', '113.00', '100.00', '58.00', '12', '5-5-0', '0', '10'], ['26', '839', '22.00', '96.00', '110.00', '136.00', '10', '6-4-0', '0', '10'], ['27', '1099', '21.00', '126.00', '110.00', '97.00', '8', '6-3-1', '0', '10'], ['28', '230', '20.00', '143.00', '80.00', '104.00', '8', '6-4-0', '0', '10'], ['29', '3017', '20.00', '134.00', '50.00', '88.00', '12', '4-6-0', '0', '10'], ['30', '2067', '20.00', '128.00', '80.00', '122.00', '10', '5-5-0', '0', '10'], ['31', '250', '20.00', '118.00', '40.00', '99.00', '10', '5-5-0', '0', '10'], ['32', '155', '20.00', '100.00', '50.00', '74.00', '12', '4-6-0', '0', '10'], ['33', '236', '20.00', '99.00', '20.00', '126.00', '10', '5-5-0', '0', '10'], ['34', '1124', '20.00', '92.00', '80.00', '109.00', '8', '6-4-0', '0', '10'], ['35', '3146', '20.00', '81.00', '110.00', '81.00', '6', '7-3-0', '0', '10'], ['36', '663', '20.00', '71.00', '90.00', '90.00', '12', '4-6-0', '0', '10'], ['37', '1699', '20.00', '70.00', '80.00', '139.00', '12', '4-6-0', '0', '10'], ['38', '1027', '20.00', '53.00', '70.00', '97.00', '12', '4-6-0', '0', '10'], ['39', '20', '19.00', '79.00', '70.00', '106.00', '9', '5-5-0', '0', '10'], ['40', '3182', '18.00', '108.00', '60.00', '147.00', '8', '5-5-0', '0', '10'], ['41', '229', '18.00', '97.00', '40.00', '153.00', '10', '4-6-0', '0', '10'], ['42', '1665', '18.00', '95.00', '120.00', '106.00', '10', '4-6-0', '0', '10'], ['43', '228', '18.00', '81.00', '60.00', '163.00', '10', '4-6-0', '0', '10'], ['44', '178', '18.00', '81.00', '50.00', '58.00', '12', '3-7-0', '0', '10'], ['45', '1740', '18.00', '62.00', '20.00', '99.00', '8', '5-5-0', '0', '10'], ['46', '3634', '18.00', '54.00', '30.00', '105.00', '10', '4-6-0', '0', '10'], ['47', '2791', '18.00', '53.00', '100.00', '108.00', '10', '4-6-0', '0', '10'], ['48', '571', '18.00', '53.00', '70.00', '109.00', '10', '4-6-0', '0', '10'], ['49', '2170', '17.00', '89.00', '60.00', '103.00', '9', '4-5-0', '1', '10'], ['50', '1493', '16.00', '150.00', '60.00', '132.00', '6', '5-5-0', '0', '10'], ['51', '549', '16.00', '129.00', '100.00', '91.00', '6', '5-5-0', '0', '10'], ['52', '743', '16.00', '70.00', '30.00', '67.00', '10', '3-7-0', '0', '10'], ['53', '2836', '16.00', '64.00', '80.00', '126.00', '8', '4-6-0', '0', '10'], ['54', '999', '14.00', '114.00', '20.00', '79.00', '10', '2-8-0', '0', '10'], ['55', '3525', '14.00', '109.00', '40.00', '66.00', '6', '4-6-0', '0', '10'], ['56', '3104', '14.00', '92.00', '20.00', '80.00', '6', '4-6-0', '0', '10'], ['57', '3555', '14.00', '68.00', '60.00', '68.00', '8', '3-7-0', '0', '10'], ['58', '4134', '13.00', '96.00', '30.00', '80.00', '6', '3-6-1', '0', '10'], ['59', '1559', '12.00', '110.00', '10.00', '94.00', '8', '2-8-0', '0', '10'], ['60', '3719', '12.00', '97.00', '60.00', '95.00', '6', '3-7-0', '0', '10'], ['61', '3654', '12.00', '59.00', '20.00', '57.00', '8', '2-8-0', '0', '10'], ['62', '2785', '12.00', '41.00', '70.00', '96.00', '8', '2-8-0', '0', '10'], ['63', '1880', '10.00', '57.00', '40.00', '86.00', '6', '2-8-0', '0', '10'], ['64', '1784', '10.00', '44.00', '40.00', '60.00', '6', '2-7-0', '1', '10']])

    def test_parse_2014casj(self):
        with open('test_data/usfirst_html/usfirst_event_rankings_2014casj.html', 'r') as f:
            rankings, _ = UsfirstEventRankingsParser.parse(f.read())

        self.assertEqual(rankings, [['Rank', 'Team', 'QS', 'ASSIST', 'AUTO', 'T&C', 'TELEOP', 'Record (W-L-T)', 'DQ', 'PLAYED'], ['1', '971', '22.00', '670.00', '650.00', '80.00', '477.00', '11-0-0', '0', '11'], ['2', '1678', '20.00', '1020.00', '541.00', '260.00', '227.00', '10-1-0', '0', '11'], ['3', '254', '20.00', '830.00', '520.00', '180.00', '505.00', '10-1-0', '0', '11'], ['4', '2035', '18.00', '750.00', '426.00', '280.00', '253.00', '9-2-0', '0', '11'], ['5', '1323', '18.00', '640.00', '435.00', '320.00', '335.00', '9-2-0', '0', '11'], ['6', '2144', '18.00', '600.00', '436.00', '180.00', '400.00', '9-2-0', '0', '11'], ['7', '192', '16.00', '610.00', '485.00', '140.00', '302.00', '8-3-0', '0', '11'], ['8', '1280', '16.00', '460.00', '387.00', '160.00', '182.00', '8-3-0', '0', '11'], ['9', '846', '16.00', '450.00', '555.00', '180.00', '381.00', '8-3-0', '0', '11'], ['10', '114', '14.00', '610.00', '401.00', '210.00', '265.00', '7-4-0', '0', '11'], ['11', '2473', '14.00', '460.00', '375.00', '190.00', '328.00', '7-4-0', '0', '11'], ['12', '4990', '14.00', '460.00', '351.00', '140.00', '378.00', '7-4-0', '0', '11'], ['13', '670', '14.00', '360.00', '470.00', '190.00', '294.00', '7-4-0', '0', '11'], ['14', '604', '14.00', '360.00', '386.00', '230.00', '301.00', '7-4-0', '0', '11'], ['15', '668', '14.00', '350.00', '500.00', '110.00', '323.00', '7-4-0', '0', '11'], ['16', '368', '12.00', '530.00', '555.00', '180.00', '468.00', '6-5-0', '0', '11'], ['17', '2489', '12.00', '470.00', '335.00', '130.00', '263.00', '6-5-0', '0', '11'], ['18', '1351', '12.00', '420.00', '330.00', '220.00', '361.00', '6-5-0', '0', '11'], ['19', '4543', '12.00', '390.00', '495.00', '190.00', '284.00', '6-5-0', '0', '11'], ['20', '2813', '12.00', '390.00', '272.00', '150.00', '199.00', '6-5-0', '0', '11'], ['21', '1388', '12.00', '380.00', '347.00', '160.00', '282.00', '6-5-0', '0', '11'], ['22', '8', '12.00', '370.00', '383.00', '180.00', '122.00', '6-5-0', '0', '11'], ['23', '3482', '12.00', '370.00', '328.00', '130.00', '259.00', '6-5-0', '0', '11'], ['24', '751', '12.00', '360.00', '307.00', '170.00', '276.00', '6-5-0', '0', '11'], ['25', '256', '12.00', '310.00', '385.00', '120.00', '263.00', '6-5-0', '0', '11'], ['26', '1700', '12.00', '280.00', '441.00', '100.00', '238.00', '6-5-0', '0', '11'], ['27', '840', '10.00', '500.00', '344.00', '50.00', '376.00', '5-6-0', '0', '11'], ['28', '3256', '10.00', '400.00', '361.00', '150.00', '388.00', '5-6-0', '0', '11'], ['29', '1662', '10.00', '370.00', '490.00', '180.00', '200.00', '5-6-0', '0', '11'], ['30', '2135', '10.00', '360.00', '307.00', '130.00', '159.00', '5-6-0', '0', '11'], ['31', '692', '10.00', '350.00', '301.00', '100.00', '218.00', '5-6-0', '0', '11'], ['32', '852', '10.00', '340.00', '361.00', '150.00', '312.00', '5-6-0', '0', '11'], ['33', '4047', '10.00', '340.00', '275.00', '150.00', '173.00', '5-6-0', '0', '11'], ['34', '1868', '10.00', '300.00', '431.00', '140.00', '247.00', '5-6-0', '0', '11'], ['35', '1072', '10.00', '300.00', '373.00', '180.00', '202.00', '5-6-0', '0', '11'], ['36', '5171', '10.00', '290.00', '376.00', '130.00', '377.00', '5-6-0', '0', '11'], ['37', '4765', '10.00', '290.00', '346.00', '110.00', '319.00', '5-6-0', '0', '11'], ['38', '766', '10.00', '280.00', '302.00', '110.00', '229.00', '5-6-0', '0', '11'], ['39', '2367', '10.00', '270.00', '366.00', '180.00', '244.00', '5-6-0', '0', '11'], ['40', '3669', '10.00', '250.00', '401.00', '120.00', '279.00', '5-6-0', '0', '11'], ['41', '4255', '10.00', '230.00', '310.00', '140.00', '226.00', '5-5-0', '1', '11'], ['42', '5311', '10.00', '120.00', '365.00', '110.00', '180.00', '5-6-0', '0', '11'], ['43', '295', '8.00', '450.00', '340.00', '90.00', '353.00', '4-7-0', '0', '11'], ['44', '100', '8.00', '310.00', '278.00', '210.00', '187.00', '4-7-0', '0', '11'], ['45', '841', '8.00', '290.00', '396.00', '120.00', '217.00', '4-7-0', '0', '11'], ['46', '5023', '8.00', '260.00', '397.00', '200.00', '224.00', '4-7-0', '0', '11'], ['47', '4904', '8.00', '260.00', '302.00', '150.00', '247.00', '4-7-0', '0', '11'], ['48', '2141', '8.00', '210.00', '220.00', '90.00', '156.00', '4-7-0', '0', '11'], ['49', '4171', '6.00', '310.00', '290.00', '70.00', '257.00', '3-8-0', '0', '11'], ['50', '5104', '6.00', '290.00', '375.00', '110.00', '289.00', '3-8-0', '0', '11'], ['51', '2854', '6.00', '280.00', '281.00', '110.00', '223.00', '3-8-0', '0', '11'], ['52', '581', '6.00', '260.00', '286.00', '120.00', '362.00', '3-8-0', '0', '11'], ['53', '115', '6.00', '210.00', '386.00', '160.00', '122.00', '3-8-0', '0', '11'], ['54', '5027', '4.00', '350.00', '361.00', '130.00', '165.00', '2-9-0', '0', '11'], ['55', '5026', '4.00', '260.00', '305.00', '120.00', '136.00', '2-9-0', '0', '11'], ['56', '3045', '4.00', '240.00', '261.00', '200.00', '184.00', '2-9-0', '0', '11'], ['57', '1967', '4.00', '220.00', '476.00', '170.00', '234.00', '2-9-0', '0', '11'], ['58', '4186', '4.00', '130.00', '251.00', '130.00', '170.00', '2-9-0', '0', '11']])