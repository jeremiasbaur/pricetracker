--
-- PostgreSQL database dump
--

-- Dumped from database version 11.2
-- Dumped by pg_dump version 11.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: company; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.company (
    id integer NOT NULL,
    name character varying NOT NULL,
    url character varying,
    scrape_url character varying NOT NULL
);


--
-- Name: company_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.company_id_seq OWNED BY public.company.id;


--
-- Name: price; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.price (
    id integer NOT NULL,
    price double precision NOT NULL,
    date timestamp without time zone NOT NULL,
    product_company_id integer
);


--
-- Name: price_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.price_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: price_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.price_id_seq OWNED BY public.price.id;


--
-- Name: product; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.product (
    id integer NOT NULL,
    name character varying NOT NULL,
    manufacturer character varying,
    manufacturer_id character varying
);


--
-- Name: product_company; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.product_company (
    id integer NOT NULL,
    product_id integer,
    company_id integer,
    tag character varying NOT NULL
);


--
-- Name: product_company_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.product_company_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: product_company_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.product_company_id_seq OWNED BY public.product_company.id;


--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.product_id_seq OWNED BY public.product.id;


--
-- Name: storage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.storage (
    id integer NOT NULL,
    company character varying NOT NULL,
    name character varying,
    keyword character varying,
    date timestamp without time zone,
    price double precision
);


--
-- Name: storage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.storage_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: storage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.storage_id_seq OWNED BY public.storage.id;


--
-- Name: company id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company ALTER COLUMN id SET DEFAULT nextval('public.company_id_seq'::regclass);


--
-- Name: price id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.price ALTER COLUMN id SET DEFAULT nextval('public.price_id_seq'::regclass);


--
-- Name: product id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product ALTER COLUMN id SET DEFAULT nextval('public.product_id_seq'::regclass);


--
-- Name: product_company id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_company ALTER COLUMN id SET DEFAULT nextval('public.product_company_id_seq'::regclass);


--
-- Name: storage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.storage ALTER COLUMN id SET DEFAULT nextval('public.storage_id_seq'::regclass);


--
-- Data for Name: company; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.company (id, name, url, scrape_url) FROM stdin;
1	Digitec	https://www.digitec.ch/	https://www.digitec.ch/de/s1/product/
2	Microspot	https://www.microspot.ch/	https://www.microspot.ch/mspocc/occ/msp/products/
3	Conrad	https://www.conrad.ch/	https://www.conrad.ch/de/
\.


--
-- Data for Name: price; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.price (id, price, date, product_company_id) FROM stdin;
9	174	2019-04-05 23:53:56.335861	1
10	571	2019-04-05 23:53:57.200911	4
11	179	2019-04-05 23:53:57.686939	6
12	101	2019-04-05 23:53:58.224969	10
13	61	2019-04-05 23:53:58.686996	13
14	75	2019-04-05 23:53:59.370035	16
15	44	2019-04-05 23:54:00.025072	19
16	179	2019-04-05 23:54:00.626107	22
17	171.90000000000001	2019-04-05 23:54:00.716112	2
18	569	2019-04-05 23:54:00.792116	5
19	179	2019-04-05 23:54:00.844119	7
20	99.400000000000006	2019-04-05 23:54:01.03313	11
21	60.899999999999999	2019-04-05 23:54:01.093133	14
22	75.200000000000003	2019-04-05 23:54:01.146136	17
23	43.899999999999999	2019-04-05 23:54:01.338147	20
24	228	2019-04-05 23:54:01.515158	23
25	179.94999999999999	2019-04-05 23:54:04.35332	8
26	171.94999999999999	2019-04-05 23:54:04.584333	9
27	119.95	2019-04-05 23:54:06.63345	12
28	73.950000000000003	2019-04-05 23:54:08.962584	15
29	71.950000000000003	2019-04-05 23:54:12.445783	18
30	41.950000000000003	2019-04-05 23:54:14.31589	21
31	174	2019-04-06 00:04:16.657342	1
32	571	2019-04-06 00:04:17.429386	4
33	179	2019-04-06 00:04:17.666399	6
34	99	2019-04-06 00:04:18.076423	10
35	61	2019-04-06 00:04:18.521448	13
36	75	2019-04-06 00:04:18.866468	16
37	44	2019-04-06 00:04:19.147484	19
38	179	2019-04-06 00:04:19.825523	22
39	171.90000000000001	2019-04-06 00:04:19.887526	2
40	569	2019-04-06 00:04:19.967531	5
41	179	2019-04-06 00:04:20.023534	7
42	99.400000000000006	2019-04-06 00:04:20.078537	11
43	60.899999999999999	2019-04-06 00:04:20.136541	14
44	75.200000000000003	2019-04-06 00:04:20.274549	17
45	43.899999999999999	2019-04-06 00:04:20.327552	20
46	228	2019-04-06 00:04:20.380555	23
47	179.94999999999999	2019-04-06 00:04:23.362725	8
48	171.94999999999999	2019-04-06 00:04:23.606739	9
49	119.95	2019-04-06 00:04:25.915871	12
50	73.950000000000003	2019-04-06 00:04:28.141999	15
51	71.950000000000003	2019-04-06 00:04:28.799036	18
52	41.950000000000003	2019-04-06 00:04:29.128055	21
53	174	2019-04-07 14:48:00.349423	1
54	569	2019-04-07 14:48:01.17847	4
55	179	2019-04-07 14:48:01.807506	6
56	101	2019-04-07 14:48:02.343537	10
57	61	2019-04-07 14:48:02.613552	13
58	75	2019-04-07 14:48:03.163584	16
59	44	2019-04-07 14:48:03.762618	19
60	179	2019-04-07 14:48:04.372653	22
61	171.90000000000001	2019-04-07 14:48:04.619667	2
62	569	2019-04-07 14:48:04.705672	5
63	179	2019-04-07 14:48:04.767676	7
64	97.450000000000003	2019-04-07 14:48:04.824679	11
65	57.600000000000001	2019-04-07 14:48:04.981688	14
66	75.200000000000003	2019-04-07 14:48:05.151698	17
67	43.899999999999999	2019-04-07 14:48:05.308707	20
68	183.94999999999999	2019-04-07 14:48:05.503718	23
69	179.94999999999999	2019-04-07 14:48:07.398826	8
70	171.94999999999999	2019-04-07 14:48:07.825851	9
71	119.95	2019-04-07 14:48:08.441886	12
72	73.950000000000003	2019-04-07 14:48:11.084037	15
73	71.950000000000003	2019-04-07 14:48:11.616067	18
74	41.950000000000003	2019-04-07 14:48:13.511176	21
75	174	2019-04-08 00:00:55.361925	1
76	571	2019-04-08 00:00:55.62794	4
77	179	2019-04-08 00:00:55.79195	6
78	99	2019-04-08 00:00:55.910957	10
79	61	2019-04-08 00:00:56.073966	13
80	75	2019-04-08 00:00:56.273977	16
81	44	2019-04-08 00:00:56.459988	19
82	179	2019-04-08 00:00:56.642998	22
83	37	2019-04-08 00:00:57.138027	25
84	299	2019-04-08 00:00:57.749062	26
85	299	2019-04-08 00:00:57.926072	28
86	171.90000000000001	2019-04-08 00:00:57.993076	2
87	569	2019-04-08 00:00:58.07808	5
88	179	2019-04-08 00:00:58.133084	7
89	97.450000000000003	2019-04-08 00:00:58.188087	11
90	57.600000000000001	2019-04-08 00:00:58.371097	14
91	75.200000000000003	2019-04-08 00:00:58.540107	17
92	43.899999999999999	2019-04-08 00:00:58.59811	20
93	183.94999999999999	2019-04-08 00:00:58.792121	23
94	679	2019-04-08 00:00:58.876126	29
95	179.94999999999999	2019-04-08 00:01:01.206259	8
96	171.94999999999999	2019-04-08 00:01:01.602282	9
97	119.95	2019-04-08 00:01:02.012306	12
98	73.950000000000003	2019-04-08 00:01:02.658342	15
99	71.950000000000003	2019-04-08 00:01:03.32138	18
100	41.950000000000003	2019-04-08 00:01:03.739404	21
101	279.94999999999999	2019-04-08 00:01:04.486447	27
129	599	2019-04-08 09:58:27.375618	125
130	927	2019-04-08 09:58:27.810643	126
131	599	2019-04-08 09:58:28.420678	127
132	2099	2019-04-08 09:58:28.899705	128
133	1649	2019-04-08 09:58:29.67975	129
134	599	2019-04-08 09:58:30.362789	130
135	1399	2019-04-08 09:58:30.878818	131
136	2099	2019-04-08 09:58:31.78087	132
137	299	2019-04-08 09:58:32.273898	133
138	749	2019-04-08 09:58:32.640919	134
139	799	2019-04-08 09:58:33.238953	135
140	749	2019-04-08 09:58:33.662978	136
141	195	2019-04-08 09:58:34.179007	137
142	1369	2019-04-08 09:58:34.858046	138
143	1299	2019-04-08 09:58:35.525084	139
144	1615	2019-04-08 09:58:36.051114	140
145	521	2019-04-08 09:58:36.562143	141
146	228	2019-04-08 09:58:37.183179	142
147	1499	2019-04-08 09:58:37.835216	143
148	1399	2019-04-08 09:58:38.295243	144
149	999	2019-04-08 09:58:38.787271	145
150	1649	2019-04-08 09:58:39.362304	146
151	2649	2019-04-08 09:58:40.00534	147
152	749	2019-04-08 09:58:40.386362	148
153	341	2019-04-08 09:58:40.942394	149
154	1549	2019-04-08 09:58:41.40542	150
155	629	2019-04-08 09:58:41.945451	151
\.


--
-- Data for Name: product; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.product (id, name, manufacturer, manufacturer_id) FROM stdin;
1	Nighthawk X6S Mesh Extender	Netgear	EX8000-100EUS
2	PowerPack (20000mAh)	ADATA	AP20000D-DGT-5V-CBK
3	Beoplay H4 Black	Bang&Olufsen	1643826
4	Galaxy S9+ (6.20", 64GB, Dual SIM, 12MP, Midnight Black)	Samsung	SM-G965FZKDAUT
5	AirPods 2nd Gen.	Apple 	MV7N2ZM/A
6	950XL/951XL Tinte	HP	C2P43AE
7	TN-241Y Toner	Brother	C2P43AE
8	Evo+ microSD 256GB	Samsung	MB-MC256GA/EU
9	Extreme 128GB	Sandisk	SDSQXA1-128G-GN6MA
10	Go 64GB	Oculus	301-00105-01
11	LC34J791 (34", 3440 x 1440 Pixels)	Samsung	LC34J791WTUXEN
111	Galaxy S9+ (6.20", 256GB, Dual SIM, 12MP, Sunrise Gold)	Samsung	SGG9650E
112	P30 Pro (6.47", 128GB, 40MP, Black)	Huawei	51093RTW
113	Galaxy S9+ (6.20", 256GB, Dual SIM, 12MP, Titanium Gray)	Samsung	SGG9650D
114	Matebook X Pro (13.90", UHD, Intel Core i7-8550U, 16GB, SSD)	Huawei	53010ESK
115	MacBook Air (13.30", Retina, Intel Core i5, 8GB, SSD)	Apple	MRE92SM/A
116	Galaxy S9 (5.80", 64GB, Dual SIM, 12MP, Midnight Black)	Samsung	SM-G960FZKDAUT
117	MacBook Air (13.30", Retina, Intel Core i5, 8GB, SSD)	Apple	MRE82SM/A
118	Surface Pro 6 Black Edition – 512GB – KJV-00018 (12.30", Intel Core i7-8650U, 16GB, SSD)	Microsoft	KJV-00018
119	Galaxy A7 (6", 64GB, Dual SIM, 24MP, Black)	Samsung	SM-A750FZKUAUT
120	P30 (6.10", 128GB, Dual SIM, 40MP, Black)	Huawei	51093NDT
121	Yoga 530-14IKB (14", Full HD, Intel Core i5-8250U, 8GB, SSD)	Lenovo	81EK00T4MZ
122	P30 (6.10", 128GB, Dual SIM, 40MP, Aurora Blue)	Huawei	51093NDR
123	Galaxy Tab A (10.10", 32GB, Metallic Black)	Samsung	SM-T580NZKEAUT
124	Mavic 2 Pro (20MP, 4K)	Dji	CP.MA.00000013.01
125	Surface Pro 6 Black Edition – 256GB – KJT-00018 (12.30", Intel Core i5-8250U, 8GB, SSD)	Microsoft	KJT-00018
126	Surface Pro 6, 256GB SSD inkl. grauem Type Cover (12.30", Intel Core i5-8250U, 8GB, SSD)	Microsoft	KJT-00003
127	8 Sirocco (5.50", 128GB, 13MP)	Nokia	11A1NB01A06
128	P20 Lite (5.80", 64GB, Dual SIM, 16MP, Midnight Black)	Huawei	51092FTN
129	ThinkPad E580 (15.60", Full HD, Intel Core i7-8550U, 32GB, SSD)	Lenovo	20KS006FMZ
130	MacBook Air (13.30", Retina, Intel Core i5, 8GB, SSD)	Apple	MREA2SM/A
131	P30 Pro (6.47", 128GB, 40MP, Breathing Crystal)	Huawei	51093RUB
132	MacBook Air (13.30", Retina, Intel Core i5, 8GB, SSD)	Apple	MREC2SM/A
133	MacBook Pro Space Grey (13.30", Retina, Intel Core i7, 16GB, SSD)	Apple	MR9Q2SM/A-140288
134	P30 (6.10", 128GB, Dual SIM, 40MP, Breathing Crystal)	Huawei	51093NDP
135	Galaxy Tab S2 Value Edition (9.70", 32GB, Weiss)	Samsung	SM-T813NZWEAUT
136	Yoga 730-15IWL (15.60", Full HD, Intel Core i7-8565U, 16GB, SSD)	Lenovo	81JS002EMZ
137	iPhone 8 (4.70", 64GB, 12MP, Space Gray)	Apple	MQ6G2ZD/A
\.


--
-- Data for Name: product_company; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.product_company (id, product_id, company_id, tag) FROM stdin;
1	1	1	6569196
2	1	2	0001403223
4	4	1	7325597
5	4	2	0001483292
6	5	1	10802238
7	5	2	0001763291
8	5	3	apple-bluetooth-kopfhoerer-in-ear-headset-weiss-1975088.html
9	1	3	netgear-ex8000-wlan-repeater-24-ghz-5-ghz-5-ghz-1604352.html
10	6	1	3230182
11	6	2	0000795625
12	6	3	hp-tinte-950xl-951xl-original-kombi-pack-schwarz-cyan-magenta-gelb-c2p43ae-1182053.html
13	7	1	416845
14	7	2	0000709313
15	7	3	brother-toner-tn-241y-tn241y-original-gelb-1400-seiten-419650.html
16	8	1	6304646
17	8	2	0001326106
18	8	3	samsung-evo-plus-microsdxc-karte-256-gb-class-10-uhs-i-uhs-class-3-inkl-sd-adapter-1547262.html
19	9	1	9706393
20	9	2	0001622579
21	9	3	sandisk-extreme-microsdxc-karte-128-gb-class-10-uhs-i-uhs-class-3-v30-video-speed-class-a2-leistungsstandard-1780912.html
22	3	1	6304953
23	3	2	0001485727
25	2	1	5988146
26	10	1	8609940
27	10	3	oculus-go-weiss-virtual-reality-brille-speicher-64-gb-inkl-controller-1716011.html
28	11	1	8609940
29	11	2	0001567355
125	111	1	9017478
126	112	1	10719630
127	113	1	9017477
128	114	1	9461708
129	115	1	10035365
130	116	1	7325593
131	117	1	10034580
132	118	1	10141349
133	119	1	9674425
134	120	1	10731465
135	121	1	9457514
136	122	1	10731563
137	123	1	7484290
138	124	1	9452335
139	125	1	10141312
140	126	1	10713853
141	127	1	7831928
142	128	1	7952043
143	129	1	7362904
144	130	1	10035411
145	131	1	10719692
146	132	1	10035414
147	133	1	9241993
148	134	1	10731472
149	135	1	5755906
150	136	1	10159010
151	137	1	5886546
\.


--
-- Data for Name: storage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.storage (id, company, name, keyword, date, price) FROM stdin;
\.


--
-- Name: company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.company_id_seq', 3, true);


--
-- Name: price_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.price_id_seq', 155, true);


--
-- Name: product_company_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.product_company_id_seq', 151, true);


--
-- Name: product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.product_id_seq', 137, true);


--
-- Name: storage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.storage_id_seq', 1, false);


--
-- Name: company company_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pkey PRIMARY KEY (id);


--
-- Name: price price_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.price
    ADD CONSTRAINT price_pkey PRIMARY KEY (id);


--
-- Name: product_company product_company_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_company
    ADD CONSTRAINT product_company_pkey PRIMARY KEY (id);


--
-- Name: product product_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- Name: storage storage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.storage
    ADD CONSTRAINT storage_pkey PRIMARY KEY (id);


--
-- Name: price price_product_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.price
    ADD CONSTRAINT price_product_company_id_fkey FOREIGN KEY (product_company_id) REFERENCES public.product_company(id);


--
-- Name: product_company product_company_company_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_company
    ADD CONSTRAINT product_company_company_id_fkey FOREIGN KEY (company_id) REFERENCES public.company(id);


--
-- Name: product_company product_company_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.product_company
    ADD CONSTRAINT product_company_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.product(id);


--
-- PostgreSQL database dump complete
--

