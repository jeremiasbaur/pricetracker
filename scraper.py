from bs4 import BeautifulSoup as bs
import traceback
import requests as r
from datastructures import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located

from selenium.webdriver.common.by import By


options = Options()
options.headless = True
geckodriver_path = r'.\Website\geckodriver-v0.24.0-win64\geckodriver.exe'

import json, time, re

class Scraper():
    engine = create_engine('postgresql://postgres:admin@localhost:5432/pricetracker_database')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)
    session = session()

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}

    driver = webdriver.Firefox(executable_path=geckodriver_path, options=options)
    wait = WebDriverWait(driver, 20)

    def __init__(self, website_url=None, scrape_base_url=None, id=None):
        if website_url is not None and scrape_base_url is not None and id is not None:
            self.info = [website_url, scrape_base_url, id]

    def get_product_company(self, product):
        """
        Gets the ProductCompany object for specific Company given a Product
        :param product: Product object
        :return: ProductCompany object for specific company
        """
        if isinstance(product, ProductCompany):
            return product
        return self.session.query(ProductCompany).filter(and_(ProductCompany.product_id == product.id, ProductCompany.company_id == self.info[2])).first()

    def scrape_price(self, product, save=False):
        """
        Scrapes the price for given product
        :param product: ProductCompany/Product object
        :param save: Save price of queried Product as new Price for this day
        :return: Price of queried product
        """
        if isinstance(product, Product):
            product = self.get_product_company(product)
        return product

    def url_product(self, product):
        """
        Gets url of product site of given product
        :param product: ProductCompany/Product object
        :return: url of product site
        """
        pass

    def scrape_for_day(self):
        """
        Scrapes all prices of Company and saves it in database
        :return: Returns failed Product id's to filter them out for future analysis
        """
        failed = []
        counter = 0
        for product in self.session.query(ProductCompany).filter(ProductCompany.company_id == self.info[2]):
            try:
                self.scrape_price(product, save=True)
            except Exception as e:
                print(f'''Failed at product: {product.tag}
                        with name: {product.product.manufacturer}
                        {product.product.name} of company:
                        {product.company.name} with error: {e}''')
                failed.append(product.product.id)
            counter += 1
            print(f'Updated {counter} products for company {product.company.name}')
        self.session.commit()
        return failed

    def scrape_by_manufacturer_id(self, product):
        """
        Scrapes and adds a new ProductCompany to DB if it's found for Company
        :param product: Product
        :return:
        """
        pass

    def insert_new_product(self, product, with_price=False):
        if isinstance(product, Product):
            results = self.scrape_by_manufacturer_id(product)
            new_product = ProductCompany(tag=results[0],
                                         product=product,
                                         company=self.session.query(Company).get(self.info[2]))
            if with_price:
                self.scrape_price(product = new_product, save = True)
            self.session.commit()

    def get_latest_price(self, product):
        product = self.get_product_company(product)
        return self.session.query(Price).filter(Price.product_company_id == product.id).order_by(Price.date.desc()).first()


class DigitecScraper(Scraper):
    def scrape_price(self, product, save=False):
        try:
            product = super().scrape_price(product)
            soup = bs(r.get(self.url_product(product), headers=self.header).content, 'html.parser')
            #print(soup.find_all('script', {'type':'application/ld+json'}))
            data = None
            for schema in soup.find_all('script', {'type': 'application/ld+json'}):
                if 'sku' in json.loads(schema.contents[0]) and str(json.loads(schema.contents[0])['sku']) == product.tag:
                    data = json.loads(schema.contents[0])
                    break

            price = min(data['offers']['lowPrice'], data['offers']['highPrice'])

        except Exception as e:
            print(f'Failed at price extraction for {self.info[0]} with product id: {product.tag} \
                    with exception {e}, url: {self.url_product(product)}')
            return None
        if save is not None and save:
            new_product_price = Price(price, datetime.datetime.now())
            product.prices.append(new_product_price)

        return price

    def url_product(self, product):
        if isinstance(product, ProductCompany):
            return self.info[1] + product.tag
        return self.info[1] + product

    def scrape_by_manufacturer_id(self, product):
        if isinstance(product, ProductCompany):
            product = self.session.query(Product).get(product.product_id)
        query_enter_search = 'query ENTER_SEARCH($query: String!, $sortOrder: ProductSort, $productTypeIds: [Int!], $brandIds: [Int!], $limit: Int = 9, $offset: Int = 0) {\n  search(query: $query, productTypeIds: $productTypeIds, brandIds: $brandIds) {\n    products(limit: $limit, offset: $offset, sortOrder: $sortOrder) {\n      total\n      hasMore\n      results {\n        ...Product\n        __typename\n      }\n      __typename\n    }\n    productTypeFilters {\n      id\n      name\n      productCount\n      __typename\n    }\n    brandFilters {\n      id\n      name\n      resultCount\n      __typename\n    }\n    help(limit: $limit, offset: $offset) {\n      total\n      results {\n        id\n        title\n        url\n        __typename\n      }\n      __typename\n    }\n    discussions(limit: $limit, offset: $offset) {\n      total\n      results {\n        ...CommunityDiscussionScored\n        __typename\n      }\n      __typename\n    }\n    questions(limit: $limit, offset: $offset) {\n      total\n      results {\n        ...CommunityQuestionScored\n        __typename\n      }\n      __typename\n    }\n    ratings(limit: $limit, offset: $offset) {\n      total\n      results {\n        ...CommunityRatingScored\n        __typename\n      }\n      __typename\n    }\n    brands(limit: $limit, offset: $offset) {\n      total\n      results {\n        id\n        title\n        __typename\n      }\n      __typename\n    }\n    magazinePages(limit: $limit, offset: $offset) {\n      total\n      hasMore\n      results {\n        ...MagazinePageScored\n        __typename\n      }\n      __typename\n    }\n    productTypes(limit: $limit, offset: $offset) {\n      total\n      results {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    tags(limit: $limit, offset: $offset) {\n      total\n      results {\n        id\n        title\n        __typename\n      }\n      __typename\n    }\n    suggestion {\n      name\n      doRedirect\n      hasResults\n      __typename\n    }\n    authors(limit: $limit, offset: $offset) {\n      total\n      results {\n        ...AuthorScored\n        __typename\n      }\n      __typename\n    }\n    redirection\n    otherPortalSuggestion {\n      numberOfFoundProducts\n      portalName\n      url\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Product on Product {\n  id\n  productTypeId\n  productTypeName\n  imageUrl\n  imageSet {\n    alternateText\n    source\n    __typename\n  }\n  sectorId\n  name\n  brandId\n  brandName\n  fullName\n  nameProperties\n  productConditionLabel\n  marketingDescription\n  pricing {\n    supplierId\n    secondHandSalesOfferId\n    price {\n      ...VatMoneySum\n      __typename\n    }\n    priceRebateFraction\n    insteadOfPrice {\n      type\n      price {\n        ...VatMoneySum\n        __typename\n      }\n      __typename\n    }\n    offerType\n    __typename\n  }\n  availability {\n    icon\n    mail {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    pickup {\n      title\n      notAllowedText\n      description\n      isAllowed\n      __typename\n    }\n    pickMup {\n      description\n      isAllowed\n      __typename\n    }\n    sites {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    isFloorDeliveryAllowed\n    __typename\n  }\n  energyEfficiency {\n    energyEfficiencyColorType\n    energyEfficiencyLabelText\n    energyEfficiencyLabelSigns\n    energyEfficiencyImageUrl\n    __typename\n  }\n  salesInformation {\n    numberOfItems\n    numberOfItemsSold\n    isLowAmountRemaining\n    __typename\n  }\n  showroomSites\n  rating\n  totalRatings\n  totalQuestions\n  isIncentiveCashback\n  incentiveText\n  isNew\n  isBestseller\n  isProductSet\n  isSalesPromotion\n  isComparable\n  isDeleted\n  isHidden\n  canAddToBasket\n  hidePrice\n  germanNames {\n    germanProductTypeName\n    nameWithoutProperties\n    germanProductNameProperties\n    germanNameWithBrand\n    __typename\n  }\n  productGroups {\n    productGroup1\n    productGroup2\n    productGroup3\n    productGroup4\n    __typename\n  }\n  __typename\n}\n\nfragment CommunityDiscussionScored on CommunityDiscussionSearchResultItem {\n  __typename\n  item {\n    ...CommunityDiscussion\n    __typename\n  }\n  searchScore\n}\n\nfragment CommunityQuestionScored on CommunityQuestionSearchResultItem {\n  __typename\n  item {\n    ...CommunityQuestion\n    __typename\n  }\n  searchScore\n}\n\nfragment CommunityRatingScored on CommunityRatingSearchResultItem {\n  __typename\n  item {\n    ...CommunityRating\n    __typename\n  }\n  searchScore\n}\n\nfragment MagazinePageScored on MagazinePagesSearchResultItem {\n  __typename\n  item {\n    ...MarketingTeaserData\n    __typename\n  }\n  searchScore\n}\n\nfragment AuthorScored on AuthorSearchResultItem {\n  __typename\n  item {\n    ...Author\n    __typename\n  }\n  searchScore\n}\n\nfragment VatMoneySum on VatMoneySum {\n  amountIncl\n  amountExcl\n  currency\n  __typename\n}\n\nfragment CommunityDiscussion on CommunityDiscussion {\n  id\n  discussionId\n  discussionEntryId\n  text\n  userId\n  insertDate\n  deleteDate\n  lastEditDate\n  upVoteCount\n  downVoteCount\n  abusiveVoteCount\n  voteScore\n  gamificationUser {\n    ...GamificationUserItem\n    __typename\n  }\n  title\n  lastActivityDate\n  numberOfAnswers\n  activeUserIds\n  numberOfFollowers\n  contextType\n  contextId\n  contextName\n  defaultSectorId\n  defaultTagIds\n  __typename\n}\n\nfragment CommunityQuestion on CommunityQuestion {\n  id\n  questionId\n  productId\n  text\n  userId\n  isEmployeeQuestion\n  insertDate\n  lastActivityDate\n  upVoteCount\n  downVoteCount\n  abusiveVoteCount\n  voteScore\n  numberOfAnswers\n  activeUserIds\n  acceptedAnswerIds\n  answerIds\n  hasAcceptedAnswers\n  gamificationUser {\n    ...GamificationUserItem\n    __typename\n  }\n  product {\n    ...CommunityProductLink\n    __typename\n  }\n  __typename\n}\n\nfragment CommunityRating on CommunityRating {\n  id\n  ratingId\n  title\n  text\n  rating\n  userId\n  insertDate\n  deleteDate\n  lastActivityDate\n  upVoteCount\n  downVoteCount\n  abusiveVoteCount\n  voteScore\n  numberOfComments\n  productId\n  activeUserIds\n  product {\n    ...CommunityProductLink\n    __typename\n  }\n  gamificationUser {\n    ...GamificationUserItem\n    __typename\n  }\n  __typename\n}\n\nfragment MarketingTeaserData on MarketingTeaserData {\n  id\n  marketingTeaserPerformanceId\n  marketingPageId\n  recommendationExplanation\n  imageUrl\n  title\n  topic\n  category\n  tagId\n  teaserLink\n  hasVideo\n  __typename\n}\n\nfragment Author on Author {\n  authorUserId\n  authorName\n  imageLink\n  authorDescription\n  jobDescription\n  authorLocation\n  __typename\n}\n\nfragment GamificationUserItem on GamificationUserItem {\n  id\n  userId\n  rank\n  level\n  activity\n  totalPointsWithDelimiter\n  achievementIcons\n  portalId\n  mandatorId\n  memberSinceDate\n  numberOfOtherAchievements\n  hasLimitedProfileView\n  userName\n  userProfileLink\n  userAvatarLink\n  userImageColorHexCode\n  isEmployee\n  employeeJobTitle\n  __typename\n}\n\nfragment CommunityProductLink on Product {\n  id\n  productTypeName\n  imageUrl\n  sectorId\n  name\n  brandName\n  fullName\n  pricing {\n    supplierId\n    secondHandSalesOfferId\n    __typename\n  }\n  __typename\n}'
        variables_enter_search = {"limit": 200, "offset": 0, "query": product.manufacturer_id}
        json_query = {'query': query_enter_search, 'variables': variables_enter_search}

        try:
            result = self.run_query_graphql(json_query)
            if len(result['data']['search']['products']['results']) == 1:
                return result['data']['search']['products']['results'][0]['id']
            return result['data']['search']['products']['results'][0]['id']
        except:
            return None

    def run_query_graphql(self, query):  # query = {'query': query_enter_search, 'variables': variables_enter_search}
        request = r.post('https://www.digitec.ch/api/graphql', json=query, headers=self.header)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    def scrape_tag_category_products(self, category, amount, offset=0):
        query_tag = 'query GET_TAG_PRODUCTS($tagId: Int!, $sectorId: Int!, $tagIdsFromNavigation: [Int!], $offset: Int, $limit: Int, $sort: ProductSort, $siteId: String) {\n  tag(id: $tagId, sectorId: $sectorId, tagIdsFromNavigation: $tagIdsFromNavigation) {\n    products(offset: $offset, limit: $limit, sort: $sort, siteId: $siteId) {\n      hasMore\n      results {\n        ...Product\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Product on Product {\n  id\n  productId\n  productTypeId\n  productTypeName\n  imageUrl\n  imageSet {\n    alternateText\n    source\n    __typename\n  }\n  sectorId\n  name\n  brandId\n  brandName\n  fullName\n  simpleName\n  nameProperties\n  productConditionLabel\n  marketingDescription\n  pricing {\n    supplierId\n    secondHandSalesOfferId\n    price {\n      ...VatMoney\n      __typename\n    }\n    priceRebateFraction\n    insteadOfPrice {\n      type\n      price {\n        ...VatMoneySum\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  availability {\n    icon\n    mail {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    pickup {\n      title\n      notAllowedText\n      description\n      isAllowed\n      __typename\n    }\n    pickMup {\n      description\n      isAllowed\n      __typename\n    }\n    sites {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    isFloorDeliveryAllowed\n    __typename\n  }\n  energyEfficiency {\n    energyEfficiencyColorType\n    energyEfficiencyLabelText\n    energyEfficiencyLabelSigns\n    energyEfficiencyImageUrl\n    __typename\n  }\n  salesInformation {\n    numberOfItems\n    numberOfItemsSold\n    isLowAmountRemaining\n    __typename\n  }\n  showroomSites\n  rating\n  totalRatings\n  totalQuestions\n  isIncentiveCashback\n  incentiveText\n  isNew\n  isBestseller\n  isProductSet\n  isSalesPromotion\n  isComparable\n  isDeleted\n  isHidden\n  canAddToBasket\n  hidePrice\n  germanNames {\n    germanProductTypeName\n    nameWithoutProperties\n    germanProductNameProperties\n    germanNameWithBrand\n    __typename\n  }\n  productGroups {\n    productGroup1\n    productGroup2\n    productGroup3\n    productGroup4\n    __typename\n  }\n  isOtherMandatorProduct\n  __typename\n}\n\nfragment VatMoney on VatMoney {\n  amountIncl\n  amountExcl\n  fraction\n  currency\n  __typename\n}\n\nfragment VatMoneySum on VatMoneySum {\n  amountIncl\n  amountExcl\n  currency\n  __typename\n}'
        variables_tag = { "tagId": category, "sectorId": 1, "tagIdsFromNavigation": [ category ], "offset": offset, "limit": amount, "sort": "BESTSELLER" }
        json_query = {'query': query_tag, 'variables': variables_tag}

        try:
            result = self.run_query_graphql(json_query)
        except Exception as e:
            print(e)
            return None

        counter = 0
        for product in result['data']['tag']['products']['results']:
            url = self.url_product(str(product['productId']))
            manufacturer_id = self.get_manufacturer_id(url)
            if manufacturer_id is None:
                continue

            if self.session.query(Product).filter(Product.manufacturer_id == manufacturer_id).first() is None:  # and self.session.query(ProductCompany).filter(and_(ProductCompany.product.manufacturer_id == manufacturer_id, ProductCompany.company_id == self.session.query(Company).get(self.info[2]).id)).first() == None:
                new_product = Product(name=product['name'], manufacturer=product['brandName'], manufacturer_id=manufacturer_id, url_image=product['imageUrl'])
                new_product_company = ProductCompany(tag=product['productId'], company=self.session.query(Company).get(self.info[2]), product=new_product, url=url)
                self.session.add_all([new_product, new_product_company])
                print(f'ADDED {counter} new product to database: Product {new_product.name} with tag: {new_product_company.tag}')
                """try:
                    self.scrape_price(new_product_company, True)
                    print("Name: %s\t Price: %f"%(product['fullName'], product['pricing']['price']['amountIncl']))
                except Exception as e:
                    print(e)
                    print("Failed at getting Price of product: %s"%(product['fullName']))"""
            else:
                print(f"NOT ADDED {counter} product: {self.session.query(Product).filter(Product.manufacturer_id == manufacturer_id).first().name} is already in database!")
            counter += 1

        self.session.commit()

    def get_manufacturer_id(self, url):
        """
        Get manufacturer_id of Product by a passed string to product
        :param url: string with url to product in shop
        :return: manufacturer_id of Product
        """
        soup = bs(r.get(url, headers=self.header).content, 'html.parser')

        try:
            data = json.loads(soup.find('script', {'id': '__NEXT_DATA__', 'type': 'application/json'}).text)
            if 'props' in data:
                for spec in data['props']['pageProps']["productDetailsData"]["specifications"]:
                    if 'title' in spec and spec['title'] == 'Allgemeine Informationen':
                        for prop in spec["properties"]:
                            if 'name' in prop and prop['name'] == "Herstellernr.":
                                manufacturer_id = prop['values'][0]['value']
                                return manufacturer_id
        except Exception as e:
            print(e)
            print(KeyError("No manufacturer_id found"))
        return None

    def scrape_image_product(self, product):
        """
        Scrapes image from Digitec servers and saves url in Product
        :param product: Product
        :return:
        """
        if type(product) != ProductCompany:
            product = self.get_product_company(product)

        soup = bs(r.get(self.url_product(product), headers=self.header).content, 'html.parser')
        # print(soup.find_all('script', {'type':'application/ld+json'}))
        data = None
        for schema in soup.find_all('script', {'type': 'application/ld+json'}):
            if 'sku' in json.loads(schema.contents[0]) and json.loads(schema.contents[0])['sku'] == int(product.tag):
                data = json.loads(schema.contents[0])
                break

        try:
            image_url = data['image'][0]
            product.product.url_image = image_url
            self.session.commit()
            print(product.product.url_image)
            return product.product.url_image
        except Exception as e:
            print(f'Failed at price extraction for {self.info[0]} with product id: {product.tag} \
                    with exception {e}, url: {self.url_product(product)}')


class MicrospotScraper(Scraper):
    def scrape_price(self, product, save=False):
        product = super().scrape_price(product)
        data = r.get(self.url_product(product), headers=self.header).json()
        price = data['price']['value']

        if save is not None and save:
            new_product_price = Price(price, datetime.datetime.now())
            product.prices.append(new_product_price)

        return price

    def url_product(self, product):
        return self.info[1] + product.tag + '?fieldSet=FULL&lang=de'

    def scrape_by_manufacturer_id(self, product, save=False):
        if isinstance(product, ProductCompany):
            product = self.session.query(Product).get(product.product_id)
        product = self.session.query(Product).get(product.id)
        query = 'https://www.microspot.ch/mspocc/occ/msp/products/search?currentPage=0&pageSize={}&query={}%20%3Arelevance&lang=de'.format(24, product.manufacturer_id)
        try:
            result = r.get(query, headers=self.header).json()
            if True or len(result['products']) == 1:
                if save:
                    if self.session.query(ProductCompany).filter(and_(ProductCompany.product_id == product.id, ProductCompany.company_id == self.session.query(Company).get(self.info[2]).id)).first() is None:
                        new_product_company = ProductCompany(tag=result['products'][0]['code'],
                                                             company=self.session.query(Company).get(self.info[2]),
                                                             product=product)
                        self.session.add(new_product_company)
                        self.session.commit()
                        self.scrape_price(product=product, save=True)
                        self.session.commit()
                return result['products'][0]['code']
        except Exception as e:
            print(e)
            return None


class ConradScraper(Scraper):
    def scrape_price(self, product, save=False):
        product = super().scrape_price(product)

        #soup = bs(r.get(self.url_product(product), headers=self.header).content, 'html.parser')
        #price = soup.find(itemprop='price').get('content')

        self.driver.get(self.url_product(product))
        self.wait.until(presence_of_element_located((By.ID, 'productPriceUnitPrice')))
        price = re.sub(r'.* ', '', self.driver.find_element_by_id('productPriceUnitPrice').text)

        if save:
            new_product_price = Price(price, datetime.datetime.now())
            product.prices.append(new_product_price)

        return price

    def url_product(self, product):
        return self.info[1] + product.tag


class PCOstschweizScraper(Scraper):
    def scrape_price(self, product, save=False):
        product = super().scrape_price(product)

        headers = {
            'Accept-Encoding' : 'gzip, deflate, br',
            'Content-Type' : 'application/x-www-form-urlencoded'
        }

        data = {
            'strType' : 'cart',
            'query' : f'pro:{product.tag};qnt:1;mth:add;',
            'rnd' : '0.15344249824532108'
        }

        cookies = r.get(url=product.url).cookies
        xml = r.get(url=self.info[1], headers=headers, params=data, cookies=cookies)
        soup = bs(xml.text, 'html.parser')

        price = float(soup.find('sumcrt').text)

        if price <= 0.0:
            raise ValueError(f"Product {product.product.name} not available at {product.company.name} anymore")

        if save:
            new_product_price = Price(price, datetime.datetime.now())
            product.prices.append(new_product_price)

        return price

    def scrape_by_manufacturer_id(self, product, save=False):
        if isinstance(product, ProductCompany):
            product = self.session.query(Product).get(product.product_id)
        product = self.session.query(Product).get(product.id)
        data = {'T': 'srch', 'suche': product.manufacturer_id}

        try:
            result = r.get(url='https://www.pc-ostschweiz.ch/de/Products.htm', headers=self.header, params=data)

            if  re.search(r'2a(\d+).htm', result.url) != None: # makes sure we actually got redirected to a specific product
                tag = re.search(r'2a(\d+).htm', result.url).group(1)

                if save:
                    if self.session.query(ProductCompany).filter(ProductCompany.product == product,
                                                             ProductCompany.company_id == self.session.query(Company).get(self.info[2]).id).first() is None:
                        new_product_company = ProductCompany(tag = tag,
                                                             company = self.session.query(Company).get(self.info[2]),
                                                             product = product, url=result.url)
                        self.session.add(new_product_company)
                        self.session.commit()
                    self.scrape_price(product = product, save = True)
                    self.session.commit()

                print(f'Found {product.name} for pcostschweiz with tag {tag}')
                return tag
            else:
                raise KeyError(f'Nothing found for product: {product.name} manufacturer_id: {product.manufacturer_id}')
        except Exception as e:
            print(e)
            return None

if __name__ == '__main__':
    engine = create_engine('postgresql://postgres:admin@localhost:5432/pricetracker_database')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)
    session = session()

    digitec = session.query(Company).filter(Company.name == 'Digitec').first()
    digitec_scraper = DigitecScraper(digitec.url, digitec.scrape_url, digitec.id)

    #digitec_scraper.scrape_tag_category_products(520, 100, 0)
    #digitec_scraper.scrape_tag_category_products(591, 100, 0)
    #digitec_scraper.scrape_tag_category_products(521, 100, 0)
    digitec_scraper.scrape_tag_category_products(1123, 300, 0)
    digitec_scraper.scrape_tag_category_products(7, 300, 0)
    digitec_scraper.scrape_tag_category_products(615, 300, 0)
    digitec_scraper.scrape_tag_category_products(1249, 300, 0)



"""
520 Fotografie
1 Gaming
591 Audio
521 Smartwatch Wearables
678 Büromaterial
1123 Drohnen
7 Netzwerk
615 PC Server
1249 Haushalt
"""
