from bs4 import BeautifulSoup as bs
import requests as r
from datastructures import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

geckodriver_path = r'.\Website\geckodriver-v0.24.0-win64\geckodriver.exe'

import json, time, re

class Scraper():
    engine = create_engine('postgresql://postgres:admin@localhost:5432/pricetracker_database')
    Base.metadata.create_all(engine)

    session = sessionmaker(engine)
    session = session()

    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    driver = webdriver.Firefox(executable_path=geckodriver_path)
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
        Scrapes all prices of company and saves it in database
        :return: Returns failed products to filter them out for future analysis
        """
        failed = []
        counter = 0
        for product in self.session.query(ProductCompany).filter(ProductCompany.company_id == self.info[2]):
            try:
                self.scrape_price(product, save=True)
            except Exception as e:
                print(f"Failed at product {product.tag} \
                        with name {self.session.query(Product).get(product.product_id).manufacturer} \
                        {self.session.query(Product).get(product.product_id).name} of company \
                        {self.session.query(Company).get(self.info[2]).name}")
                failed.append(self.session.query(Product).get(product.product_id))
            counter += 1
            print('Updated %d products for company %s' % (counter, self.session.query(Company).get(self.info[2]).name))
            # time.sleep(0.4)
        self.session.commit()
        return failed

    def scrape_by_manufacturer_id(self, product):
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
        product = super().scrape_price(product)
        soup = bs(r.get(self.url_product(product), headers=self.header).content, 'html.parser')
        # print(soup.find_all('script', {'type':'application/ld+json'}))
        data = None
        for schema in soup.find_all('script', {'type': 'application/ld+json'}):
            if 'sku' in json.loads(schema.contents[0]) and json.loads(schema.contents[0])['sku'] == int(product.tag):
                data = json.loads(schema.contents[0])
                break

        try:
            price = data['offers']['lowPrice']
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
        variables_enter_search = { "limit": 200, "offset": 0, "query": product.manufacturer_id }
        json_query = {'query': query_enter_search, 'variables': variables_enter_search}

        try:
            result = self.run_query_graphql(json_query)
            if len(result['data']['search']['products']['results']) == 1:
                return result['data']['search']['products']['results'][0]['id']
            return result['data']['search']['products']['results'][0]['id']
        except:
            return None

    def run_query_graphql(self, query): # query = {'query': query_enter_search, 'variables': variables_enter_search}
        request = r.post('https://www.digitec.ch/api/graphql', json=query, headers=self.header)
        if request.status_code == 200:
            return request.json()
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

    def scrape_tag_category_products(self, category, amount, offset=0):
        query_tag = 'query GET_TAG_PRODUCTS($tagId: Int!, $sectorId: Int!, $tagIdsFromNavigation: [Int!], $offset: Int, $limit: Int, $sort: ProductSort, $siteId: String) {\n  tag(id: $tagId, sectorId: $sectorId, tagIdsFromNavigation: $tagIdsFromNavigation) {\n    products(offset: $offset, limit: $limit, sort: $sort, siteId: $siteId) {\n      hasMore\n      results {\n        ...Product\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Product on Product {\n  id\n  productTypeId\n  productTypeName\n  imageUrl\n  imageSet {\n    alternateText\n    source\n    __typename\n  }\n  sectorId\n  name\n  brandId\n  brandName\n  fullName\n  nameProperties\n  productConditionLabel\n  marketingDescription\n  pricing {\n    supplierId\n    secondHandSalesOfferId\n    price {\n      ...VatMoneySum\n      __typename\n    }\n    priceRebateFraction\n    insteadOfPrice {\n      type\n      price {\n        ...VatMoneySum\n        __typename\n      }\n      __typename\n    }\n    offerType\n    __typename\n  }\n  availability {\n    icon\n    mail {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    pickup {\n      title\n      notAllowedText\n      description\n      isAllowed\n      __typename\n    }\n    pickMup {\n      description\n      isAllowed\n      __typename\n    }\n    sites {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    isFloorDeliveryAllowed\n    __typename\n  }\n  energyEfficiency {\n    energyEfficiencyColorType\n    energyEfficiencyLabelText\n    energyEfficiencyLabelSigns\n    energyEfficiencyImageUrl\n    __typename\n  }\n  salesInformation {\n    numberOfItems\n    numberOfItemsSold\n    isLowAmountRemaining\n    __typename\n  }\n  showroomSites\n  rating\n  totalRatings\n  totalQuestions\n  isIncentiveCashback\n  incentiveText\n  isNew\n  isBestseller\n  isProductSet\n  isSalesPromotion\n  isComparable\n  isDeleted\n  isHidden\n  canAddToBasket\n  hidePrice\n  germanNames {\n    germanProductTypeName\n    nameWithoutProperties\n    germanProductNameProperties\n    germanNameWithBrand\n    __typename\n  }\n  productGroups {\n    productGroup1\n    productGroup2\n    productGroup3\n    productGroup4\n    __typename\n  }\n  __typename\n}\n\nfragment VatMoneySum on VatMoneySum {\n  amountIncl\n  amountExcl\n  currency\n  __typename\n}'
        variables_tag = { "tagId": category, "sectorId": 1, "tagIdsFromNavigation": [ category ], "offset": offset, "limit": amount, "sort": "BESTSELLER" }
        json_query = {'query': query_tag, 'variables': variables_tag}
        print("in category")
        try:
            print("before query")
            result = self.run_query_graphql(json_query)
            print("after query")
            counter = 0
            for product in result['data']['tag']['products']['results']:
                print(self.url_product(product['id']))
                manufacturer_id = self.scrape_manufacturer_id_url(self.url_product(product['id']))

                if manufacturer_id is None:
                    continue
                if self.session.query(Product).filter(Product.manufacturer_id == manufacturer_id).first() is None: #and self.session.query(ProductCompany).filter(and_(ProductCompany.product.manufacturer_id == manufacturer_id, ProductCompany.company_id == self.session.query(Company).get(self.info[2]).id)).first() == None:
                    print("add %i"%counter)
                    new_product = Product(name=product['name'], manufacturer=product['brandName'], manufacturer_id=manufacturer_id)
                    new_product_company = ProductCompany(tag=product['id'], company=self.session.query(Company).get(self.info[2]), product=new_product)
                    self.session.add_all([new_product, new_product_company])
                    try:
                        self.scrape_price(new_product_company, True)
                        print("Name: %s\t Price: %f"%(product['fullName'], product['pricing']['price']['amountIncl']))
                    except Exception as e:
                        print(e)
                        print("Failed at getting Price of product: %s"%(product['fullName']))
                else:
                    print("already in database")
                counter += 1

        except Exception as e:
            print(e)
            self.session.rollback()
            return None
        self.session.commit()

    def scrape_manufacturer_id_url(self, url):
        soup = bs(r.get(url, headers=self.header).content, 'html.parser')
        try:
            manufacturer_id = soup.find('td', text='Herstellernr.').find_next_sibling("td").text
        except:
            return None
        #if save!= None and save:
        #    new_product_price = Price(price, datetime.datetime.now())
        #    product.prices.append(new_product_price)
        return manufacturer_id

    def scrape_image_product(self, product):
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
        data = r.get(self.url_product(product), headers = self.header).json()
        price = data['price']['value']

        if save!= None and save:
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
                        new_product_company = ProductCompany(tag=result['products'][0]['code'], company=self.session.query(Company).get(self.info[2]), product= product)
                        self.session.add(new_product_company)
                        self.session.commit()
                        self.scrape_price(product = product, save = True)
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

if __name__ == '__main__':
    """if response.history:
        print("Request was redirected")
        for resp in response.history:
            print(resp.status_code, resp.url)
        print("Final destination:")
        print(response.status_code, response.url)
    else:
        print("Request was not redirected")"""
    digitec = DigitecScraper('https://www.digitec.ch/', 'https://www.digitec.ch/de/s1/product/')
    print(digitec.scrape_price(1))
    conrad = ConradScraper('https://www.conrad.ch/', 'https://www.conrad.ch/de/')
    print(conrad.scrape_price(1))
    microspot = MicrospotScraper('https://www.microspot.ch/', 'https://www.microspot.ch/mspocc/occ/msp/products/')
    print(microspot.scrape_price(1))
