# An example to get the remaining rate limit using the Github GraphQL API.
import requests, re

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def run_query(query): # A simple function to use requests.post to make the API call. Note the json= section.
    request = requests.post('https://www.digitec.ch/api/graphql', json=json_query, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


# The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.
query_search = """
query PRODUCTS_SEARCH($query: String!, $sortOrder: ProductSort, $productTypeIds: [Int!], $brandIds: [Int!], $limit: Int = 45, $offset: Int) {
  search(query: $query, productTypeIds: $productTypeIds, brandIds: $brandIds) {
    products(limit: $limit, offset: $offset, sortOrder: $sortOrder) {
      total
      hasMore
      results {
        ...Product
        __typename
      }
      __typename
    }
    productTypeFilters {
      id
      productCount
      __typename
    }
    brandFilters {
      id
      resultCount
      __typename
    }
    __typename
  }
}

fragment Product on Product {
  id
  productTypeId
  productTypeName
  imageUrl
  imageSet {
    alternateText
    source
    __typename
  }
  sectorId
  name
  brandId
  brandName
  fullName
  nameProperties
  productConditionLabel
  marketingDescription
  pricing {
    supplierId
    secondHandSalesOfferId
    price {
      ...VatMoneySum
      __typename
    }
    priceRebateFraction
    insteadOfPrice {
      type
      price {
        ...VatMoneySum
        __typename
      }
      __typename
    }
    offerType
    __typename
  }
  availability {
    icon
    mail {
      siteId
      title
      type
      icon
      text
      description
      tooltipDescription
      numberOfItems
      deliveryDate
      __typename
    }
    pickup {
      title
      notAllowedText
      description
      isAllowed
      __typename
    }
    pickMup {
      description
      isAllowed
      __typename
    }
    sites {
      siteId
      title
      type
      icon
      text
      description
      tooltipDescription
      numberOfItems
      deliveryDate
      __typename
    }
    isFloorDeliveryAllowed
    __typename
  }
  energyEfficiency {
    energyEfficiencyColorType
    energyEfficiencyLabelText
    energyEfficiencyLabelSigns
    energyEfficiencyImageUrl
    __typename
  }
  salesInformation {
    numberOfItems
    numberOfItemsSold
    isLowAmountRemaining
    __typename
  }
  showroomSites
  rating
  totalRatings
  totalQuestions
  isIncentiveCashback
  incentiveText
  isNew
  isBestseller
  isProductSet
  isSalesPromotion
  isComparable
  isDeleted
  isHidden
  canAddToBasket
  hidePrice
  germanNames {
    germanProductTypeName
    nameWithoutProperties
    germanProductNameProperties
    germanNameWithBrand
    __typename
  }
  productGroups {
    productGroup1
    productGroup2
    productGroup3
    productGroup4
    __typename
  }
  __typename
}

fragment VatMoneySum on VatMoneySum {
  amountIncl
  amountExcl
  currency
  __typename
}"""
query = """query GET_PRODUCTS($productIds: [Int!]!, $offset: Int, $limit: Int, $sort: ProductSort, $siteId: String) {
  products(productIds: $productIds, offset: $offset, limit: $limit, sort: $sort, siteId: $siteId) {
    total
    products {
      ...Product
      __typename
    }
    __typename
  }
}

fragment Product on Product {
  id
  productTypeId
  productTypeName
  imageUrl
  imageSet {
    alternateText
    source
    __typename
  }
  sectorId
  name
  brandId
  brandName
  fullName
  nameProperties
  productConditionLabel
  marketingDescription
  pricing {
    supplierId
    secondHandSalesOfferId
    price {
      ...VatMoneySum
      __typename
    }
    priceRebateFraction
    insteadOfPrice {
      type
      price {
        ...VatMoneySum
        __typename
      }
      __typename
    }
    offerType
    __typename
  }
  availability {
    icon
    mail {
      siteId
      title
      type
      icon
      text
      description
      tooltipDescription
      numberOfItems
      deliveryDate
      __typename
    }
    pickup {
      title
      notAllowedText
      description
      isAllowed
      __typename
    }
    pickMup {
      description
      isAllowed
      __typename
    }
    sites {
      siteId
      title
      type
      icon
      text
      description
      tooltipDescription
      numberOfItems
      deliveryDate
      __typename
    }
    isFloorDeliveryAllowed
    __typename
  }
  energyEfficiency {
    energyEfficiencyColorType
    energyEfficiencyLabelText
    energyEfficiencyLabelSigns
    energyEfficiencyImageUrl
    __typename
  }
  salesInformation {
    numberOfItems
    numberOfItemsSold
    isLowAmountRemaining
    __typename
  }
  showroomSites
  rating
  totalRatings
  totalQuestions
  isIncentiveCashback
  incentiveText
  isNew
  isBestseller
  isProductSet
  isSalesPromotion
  isComparable
  isDeleted
  isHidden
  canAddToBasket
  hidePrice
  germanNames {
    germanProductTypeName
    nameWithoutProperties
    germanProductNameProperties
    germanNameWithBrand
    __typename
  }
  productGroups {
    productGroup1
    productGroup2
    productGroup3
    productGroup4
    __typename
  }
  __typename
}

fragment VatMoneySum on VatMoneySum {
  amountIncl
  amountExcl
  currency
  __typename
}
"""
variables = {
    "productIds": [
        10296605,
        10174951,
        8609940,
        9387981,
        9923818,
        8613755,
        7042098,
        10873347,
        6521992,
        9398808,
        5988146,
        3230182,
        6304953,
        7325597,
        307639,
        5815948,
        434178,
        9706393,
        6304646,
        416844
    ],
    "sort": "PRESERVEORDERING"
}

query_enter_search = 'query ENTER_SEARCH($query: String!, $sortOrder: ProductSort, $productTypeIds: [Int!], $brandIds: [Int!], $limit: Int = 9, $offset: Int = 0) {\n  search(query: $query, productTypeIds: $productTypeIds, brandIds: $brandIds) {\n    products(limit: $limit, offset: $offset, sortOrder: $sortOrder) {\n      total\n      hasMore\n      results {\n        ...Product\n        __typename\n      }\n      __typename\n    }\n    productTypeFilters {\n      id\n      name\n      productCount\n      __typename\n    }\n    brandFilters {\n      id\n      name\n      resultCount\n      __typename\n    }\n    help(limit: $limit, offset: $offset) {\n      total\n      results {\n        id\n        title\n        url\n        __typename\n      }\n      __typename\n    }\n    discussions(limit: $limit, offset: $offset) {\n      total\n      results {\n        ...CommunityDiscussionScored\n        __typename\n      }\n      __typename\n    }\n    questions(limit: $limit, offset: $offset) {\n      total\n      results {\n        ...CommunityQuestionScored\n        __typename\n      }\n      __typename\n    }\n    ratings(limit: $limit, offset: $offset) {\n      total\n      results {\n        ...CommunityRatingScored\n        __typename\n      }\n      __typename\n    }\n    brands(limit: $limit, offset: $offset) {\n      total\n      results {\n        id\n        title\n        __typename\n      }\n      __typename\n    }\n    magazinePages(limit: $limit, offset: $offset) {\n      total\n      hasMore\n      results {\n        ...MagazinePageScored\n        __typename\n      }\n      __typename\n    }\n    productTypes(limit: $limit, offset: $offset) {\n      total\n      results {\n        id\n        name\n        __typename\n      }\n      __typename\n    }\n    tags(limit: $limit, offset: $offset) {\n      total\n      results {\n        id\n        title\n        __typename\n      }\n      __typename\n    }\n    suggestion {\n      name\n      doRedirect\n      hasResults\n      __typename\n    }\n    authors(limit: $limit, offset: $offset) {\n      total\n      results {\n        ...AuthorScored\n        __typename\n      }\n      __typename\n    }\n    redirection\n    otherPortalSuggestion {\n      numberOfFoundProducts\n      portalName\n      url\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Product on Product {\n  id\n  productTypeId\n  productTypeName\n  imageUrl\n  imageSet {\n    alternateText\n    source\n    __typename\n  }\n  sectorId\n  name\n  brandId\n  brandName\n  fullName\n  nameProperties\n  productConditionLabel\n  marketingDescription\n  pricing {\n    supplierId\n    secondHandSalesOfferId\n    price {\n      ...VatMoneySum\n      __typename\n    }\n    priceRebateFraction\n    insteadOfPrice {\n      type\n      price {\n        ...VatMoneySum\n        __typename\n      }\n      __typename\n    }\n    offerType\n    __typename\n  }\n  availability {\n    icon\n    mail {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    pickup {\n      title\n      notAllowedText\n      description\n      isAllowed\n      __typename\n    }\n    pickMup {\n      description\n      isAllowed\n      __typename\n    }\n    sites {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    isFloorDeliveryAllowed\n    __typename\n  }\n  energyEfficiency {\n    energyEfficiencyColorType\n    energyEfficiencyLabelText\n    energyEfficiencyLabelSigns\n    energyEfficiencyImageUrl\n    __typename\n  }\n  salesInformation {\n    numberOfItems\n    numberOfItemsSold\n    isLowAmountRemaining\n    __typename\n  }\n  showroomSites\n  rating\n  totalRatings\n  totalQuestions\n  isIncentiveCashback\n  incentiveText\n  isNew\n  isBestseller\n  isProductSet\n  isSalesPromotion\n  isComparable\n  isDeleted\n  isHidden\n  canAddToBasket\n  hidePrice\n  germanNames {\n    germanProductTypeName\n    nameWithoutProperties\n    germanProductNameProperties\n    germanNameWithBrand\n    __typename\n  }\n  productGroups {\n    productGroup1\n    productGroup2\n    productGroup3\n    productGroup4\n    __typename\n  }\n  __typename\n}\n\nfragment CommunityDiscussionScored on CommunityDiscussionSearchResultItem {\n  __typename\n  item {\n    ...CommunityDiscussion\n    __typename\n  }\n  searchScore\n}\n\nfragment CommunityQuestionScored on CommunityQuestionSearchResultItem {\n  __typename\n  item {\n    ...CommunityQuestion\n    __typename\n  }\n  searchScore\n}\n\nfragment CommunityRatingScored on CommunityRatingSearchResultItem {\n  __typename\n  item {\n    ...CommunityRating\n    __typename\n  }\n  searchScore\n}\n\nfragment MagazinePageScored on MagazinePagesSearchResultItem {\n  __typename\n  item {\n    ...MarketingTeaserData\n    __typename\n  }\n  searchScore\n}\n\nfragment AuthorScored on AuthorSearchResultItem {\n  __typename\n  item {\n    ...Author\n    __typename\n  }\n  searchScore\n}\n\nfragment VatMoneySum on VatMoneySum {\n  amountIncl\n  amountExcl\n  currency\n  __typename\n}\n\nfragment CommunityDiscussion on CommunityDiscussion {\n  id\n  discussionId\n  discussionEntryId\n  text\n  userId\n  insertDate\n  deleteDate\n  lastEditDate\n  upVoteCount\n  downVoteCount\n  abusiveVoteCount\n  voteScore\n  gamificationUser {\n    ...GamificationUserItem\n    __typename\n  }\n  title\n  lastActivityDate\n  numberOfAnswers\n  activeUserIds\n  numberOfFollowers\n  contextType\n  contextId\n  contextName\n  defaultSectorId\n  defaultTagIds\n  __typename\n}\n\nfragment CommunityQuestion on CommunityQuestion {\n  id\n  questionId\n  productId\n  text\n  userId\n  isEmployeeQuestion\n  insertDate\n  lastActivityDate\n  upVoteCount\n  downVoteCount\n  abusiveVoteCount\n  voteScore\n  numberOfAnswers\n  activeUserIds\n  acceptedAnswerIds\n  answerIds\n  hasAcceptedAnswers\n  gamificationUser {\n    ...GamificationUserItem\n    __typename\n  }\n  product {\n    ...CommunityProductLink\n    __typename\n  }\n  __typename\n}\n\nfragment CommunityRating on CommunityRating {\n  id\n  ratingId\n  title\n  text\n  rating\n  userId\n  insertDate\n  deleteDate\n  lastActivityDate\n  upVoteCount\n  downVoteCount\n  abusiveVoteCount\n  voteScore\n  numberOfComments\n  productId\n  activeUserIds\n  product {\n    ...CommunityProductLink\n    __typename\n  }\n  gamificationUser {\n    ...GamificationUserItem\n    __typename\n  }\n  __typename\n}\n\nfragment MarketingTeaserData on MarketingTeaserData {\n  id\n  marketingTeaserPerformanceId\n  marketingPageId\n  recommendationExplanation\n  imageUrl\n  title\n  topic\n  category\n  tagId\n  teaserLink\n  hasVideo\n  __typename\n}\n\nfragment Author on Author {\n  authorUserId\n  authorName\n  imageLink\n  authorDescription\n  jobDescription\n  authorLocation\n  __typename\n}\n\nfragment GamificationUserItem on GamificationUserItem {\n  id\n  userId\n  rank\n  level\n  activity\n  totalPointsWithDelimiter\n  achievementIcons\n  portalId\n  mandatorId\n  memberSinceDate\n  numberOfOtherAchievements\n  hasLimitedProfileView\n  userName\n  userProfileLink\n  userAvatarLink\n  userImageColorHexCode\n  isEmployee\n  employeeJobTitle\n  __typename\n}\n\nfragment CommunityProductLink on Product {\n  id\n  productTypeName\n  imageUrl\n  sectorId\n  name\n  brandName\n  fullName\n  pricing {\n    supplierId\n    secondHandSalesOfferId\n    __typename\n  }\n  __typename\n}'
variables_enter_search = { "limit": 24, "offset": 0, "query": "1643826" }

query_top_category = """query GET_PRODUCT_TYPE_PRODUCTS_AND_FILTERS($productTypeId: Int!, $queryString: String!, $stickyFilterString: String!, $offset: Int, $limit: Int, $sort: ProductSort, $siteId: String) {
  productType(id: $productTypeId) {
    filterProducts(queryString: $queryString, stickyFilterString: $stickyFilterString, offset: $offset, limit: $limit, sort: $sort, siteId: $siteId) {
      productCounts {
        total
        filteredTotal
        __typename
      }
      filterSelection {
        featuredFilter {
          ...Filter
          __typename
        }
        filterGroups {
          ...FilterGroup
          __typename
        }
        __typename
      }
      products {
        hasMore
        results {
          ...Product
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment Filter on Filter {
  optionIdentifierKey
  optionIdentifierValue
  label
  productCount
  selected
  isSticky
  tooltipText
  tooltipMoreInformationLink
  __typename
}

fragment FilterGroup on FilterGroup {
  key
  label
  tooltipContent
  tooltipMoreInformationLink
  filterOptions {
    ...Filter
    __typename
  }
  __typename
}

fragment Product on Product {
  id
  productTypeId
  productTypeName
  imageUrl
  imageSet {
    alternateText
    source
    __typename
  }
  sectorId
  name
  brandId
  brandName
  fullName
  nameProperties
  productConditionLabel
  marketingDescription
  pricing {
    supplierId
    secondHandSalesOfferId
    price {
      ...VatMoneySum
      __typename
    }
    priceRebateFraction
    insteadOfPrice {
      type
      price {
        ...VatMoneySum
        __typename
      }
      __typename
    }
    offerType
    __typename
  }
  availability {
    icon
    mail {
      siteId
      title
      type
      icon
      text
      description
      tooltipDescription
      numberOfItems
      deliveryDate
      __typename
    }
    pickup {
      title
      notAllowedText
      description
      isAllowed
      __typename
    }
    pickMup {
      description
      isAllowed
      __typename
    }
    sites {
      siteId
      title
      type
      icon
      text
      description
      tooltipDescription
      numberOfItems
      deliveryDate
      __typename
    }
    isFloorDeliveryAllowed
    __typename
  }
  energyEfficiency {
    energyEfficiencyColorType
    energyEfficiencyLabelText
    energyEfficiencyLabelSigns
    energyEfficiencyImageUrl
    __typename
  }
  salesInformation {
    numberOfItems
    numberOfItemsSold
    isLowAmountRemaining
    __typename
  }
  showroomSites
  rating
  totalRatings
  totalQuestions
  isIncentiveCashback
  incentiveText
  isNew
  isBestseller
  isProductSet
  isSalesPromotion
  isComparable
  isDeleted
  isHidden
  canAddToBasket
  hidePrice
  germanNames {
    germanProductTypeName
    nameWithoutProperties
    germanProductNameProperties
    germanNameWithBrand
    __typename
  }
  productGroups {
    productGroup1
    productGroup2
    productGroup3
    productGroup4
    __typename
  }
  __typename
}

fragment VatMoneySum on VatMoneySum {
  amountIncl
  amountExcl
  currency
  __typename
}"""
variables_top_category = """{
    "productTypeId": 24,
    "queryString": "",
    "stickyFilterString": "",
    "offset": 0,
    "limit": 3000,
    "sort": "BESTSELLER",
    "siteId": null
}""" # 24 mobiltelefone, 304 handyhüllen, 678 bürobedarf,

query_tag = 'query GET_TAG_PRODUCTS($tagId: Int!, $sectorId: Int!, $tagIdsFromNavigation: [Int!], $offset: Int, $limit: Int, $sort: ProductSort, $siteId: String) {\n  tag(id: $tagId, sectorId: $sectorId, tagIdsFromNavigation: $tagIdsFromNavigation) {\n    products(offset: $offset, limit: $limit, sort: $sort, siteId: $siteId) {\n      hasMore\n      results {\n        ...Product\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment Product on Product {\n  id\n  productTypeId\n  productTypeName\n  imageUrl\n  imageSet {\n    alternateText\n    source\n    __typename\n  }\n  sectorId\n  name\n  brandId\n  brandName\n  fullName\n  nameProperties\n  productConditionLabel\n  marketingDescription\n  pricing {\n    supplierId\n    secondHandSalesOfferId\n    price {\n      ...VatMoneySum\n      __typename\n    }\n    priceRebateFraction\n    insteadOfPrice {\n      type\n      price {\n        ...VatMoneySum\n        __typename\n      }\n      __typename\n    }\n    offerType\n    __typename\n  }\n  availability {\n    icon\n    mail {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    pickup {\n      title\n      notAllowedText\n      description\n      isAllowed\n      __typename\n    }\n    pickMup {\n      description\n      isAllowed\n      __typename\n    }\n    sites {\n      siteId\n      title\n      type\n      icon\n      text\n      description\n      tooltipDescription\n      numberOfItems\n      deliveryDate\n      __typename\n    }\n    isFloorDeliveryAllowed\n    __typename\n  }\n  energyEfficiency {\n    energyEfficiencyColorType\n    energyEfficiencyLabelText\n    energyEfficiencyLabelSigns\n    energyEfficiencyImageUrl\n    __typename\n  }\n  salesInformation {\n    numberOfItems\n    numberOfItemsSold\n    isLowAmountRemaining\n    __typename\n  }\n  showroomSites\n  rating\n  totalRatings\n  totalQuestions\n  isIncentiveCashback\n  incentiveText\n  isNew\n  isBestseller\n  isProductSet\n  isSalesPromotion\n  isComparable\n  isDeleted\n  isHidden\n  canAddToBasket\n  hidePrice\n  germanNames {\n    germanProductTypeName\n    nameWithoutProperties\n    germanProductNameProperties\n    germanNameWithBrand\n    __typename\n  }\n  productGroups {\n    productGroup1\n    productGroup2\n    productGroup3\n    productGroup4\n    __typename\n  }\n  __typename\n}\n\nfragment VatMoneySum on VatMoneySum {\n  amountIncl\n  amountExcl\n  currency\n  __typename\n}'
variables_tag = { "tagId": 1, "sectorId": 1, "tagIdsFromNavigation": [ 1 ], "offset": 0, "limit": 1, "sort": "BESTSELLER"}

json_query = {'query': query_tag, 'variables': variables_tag}

#result = run_query(json_query) # Execute the query

query = 'https://www.microspot.ch/mspocc/occ/msp/products/search?currentPage=0&pageSize={}&query={}%20%3Arelevance&lang=de'.format(24, "20M7001EMZ")

#print(requests.get(query, headers=headers).json())
#remaining_rate_limit = result["data"]["rateLimit"]["remaining"] # Drill down the dictionary
#print("Remaining rate limit - {}".format(remaining_rate_limit))
#print(result)
#print(result)
#print(result['data']['search']['products']['results'][0]['pricing']['price']['amountIncl']) # search
#print(len(result['data']['search']['products']['results'])) # search
#print(len(result['data']['productType']['filterProducts']['products']['results'])) # search

# top category
#for product in result['data']['productType']['filterProducts']['products']['results']:
#    print("Name: %s\t Price: %f"%(product['fullName'], product['pricing']['price']['amountIncl']))

# tag category
#for product in result['data']['tag']['products']['results']:
#    print("Name: %s\t Price: %f"%(product['fullName'], product['pricing']['price']['amountIncl']))

print(re.sub(r'.* ', '', 'CHF 201.5'))
