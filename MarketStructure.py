import math

doubleBottomParameters = {
    "bottomsHeightThreshold": 0.95,
    "breakoutHeightThreshold": 0.9,
    "midPointHeightThreshold": 0.9
}

def advancedDoubleBottom(prices, symbol):
    allBottoms = []
    
    lowestPoint = {"value": prices[0], "index": 0}
    bottomsHeightThreshold = doubleBottomParameters["bottomsHeightThreshold"]
    bottomsWidthThreshold = math.floor(len(prices)/3) #bars
    midPointHeightThreshold = doubleBottomParameters["midPointHeightThreshold"]
    breakoutHeightThreshold = doubleBottomParameters["breakoutHeightThreshold"]
    currentPrice = prices[0]
    
    for i in range(len(prices)):
        index = len(prices) - i - 1
        price = prices[index]
        
        # Update lowest point
        if price < lowestPoint['value']:
            lowestPoint = {"value": price, "index": index}
        
        if index < len(prices) - 1 and index > 0:
            mid = price
            right = prices[index + 1]
            left = prices[index -1]
            if isEmpireBottom(mid, left, right):
                allBottoms.append({"value": mid, "index": index})
    
    for i in range(len(allBottoms)):
        leadingBottom = allBottoms[i]
        laggingBottom = findCorrespondingLaggingBottom(leadingBottom, i, allBottoms, bottomsHeightThreshold, bottomsWidthThreshold)
        if laggingBottom is None:
            continue
        midPoint = findMidpoint(laggingBottom, leadingBottom, prices)
        breakout = findBreakout(leadingBottom, prices)
        # if pass, return, if not, keep looking
        state = (
            leadingBottom is not None
            and laggingBottom is not None
            and midPoint is not None
            and midPoint['value'] > leadingBottom['value']
            and breakout['value'] > midPoint['value'] 
            and lowestPoint['index'] <= laggingBottom['index']
            and 1 > leadingBottom['value'] / midPoint['value'] >= midPointHeightThreshold 
            and 1 >= midPoint['value'] / breakout['value'] >= breakoutHeightThreshold
            and currentPrice > laggingBottom['value']
        )
        if state is True:
            return {
                "state": state,
                "laggingBottomPrice": laggingBottom['value'] if laggingBottom is not None else None,
                "leadingBottomPrice": leadingBottom['value'] if leadingBottom is not None else None,
                "midPointPrice": midPoint['value'] if midPoint is not None else None,
                "breakoutPrice": breakout['value'] if breakout is not None else None,
                "currentPrice": currentPrice
            }
            
    return {"state": False}
    

def basicDoubleBottom(prices):
    '''
    leadingBottom must be higher than (threshold), to the right of, and at least 10 bars apart from laggingBottom
    Midpoint must be in between both bottoms and higher than both
    Breakout must be above mid point and to the right of leadingBottom
    lowestPoit msut be to the left of lagging bottom or lagging bottom
    '''
    leadingBottom = None
    laggingBottom = None
    midPoint = None
    breakout = None
    lowestPoint = {"value": prices[0], "index": 0}
    bottomsHeightThreshold = doubleBottomParameters["bottomsHeightThreshold"]
    bottomsWidthThreshold = math.floor(len(prices)/3) #bars
    midPointHeightThreshold = doubleBottomParameters["midPointHeightThreshold"]
    breakoutHeightThreshold = doubleBottomParameters["breakoutHeightThreshold"]
    currentPrice = prices[0]
        
    for i in range(len(prices)):
        index = len(prices) - i - 1
        price = prices[index]
        
        # Update lowest point
        if price < lowestPoint['value']:
            lowestPoint = {"value": price, "index": index}
               
        if index < len(prices) - 1 and index > 0:
            mid = price
            right = prices[index + 1]
            left = prices[index -1]
            if isEmpireBottom(mid, left, right):
                # Set leading bottom
                if leadingBottom is None:
                    leadingBottom = {"value": price, "index": index}
                    continue
                if laggingBottom is None:
                    # lagging bottom is lower than
                    if (
                            1 >= mid / leadingBottom['value'] >= bottomsHeightThreshold 
                            and index + bottomsWidthThreshold <= leadingBottom["index"]
                        ):
                            laggingBottom = {"value": price, "index": index}
                            midPoint = findMidpoint(laggingBottom, leadingBottom, prices)
                            breakout = findBreakout(leadingBottom, prices)
                            break
    
    state = (
        leadingBottom is not None
        and laggingBottom is not None
        and midPoint is not None
        and midPoint['value'] > leadingBottom['value']
        and breakout['value'] > midPoint['value'] 
        and lowestPoint['index'] <= laggingBottom['index']
        and 1 > leadingBottom['value'] / midPoint['value'] >= midPointHeightThreshold 
        and 1 >= midPoint['value'] / breakout['value'] >= breakoutHeightThreshold
        and currentPrice > laggingBottom['value']
    )
        
    return {
        "state": state,
        "laggingBottomPrice": laggingBottom['value'] if laggingBottom is not None else None,
        "leadingBottomPrice": leadingBottom['value'] if leadingBottom is not None else None,
        "midPointPrice": midPoint['value'] if midPoint is not None else None,
        "breakoutPrice": breakout['value'] if breakout is not None else None,
        "currentPrice": currentPrice
    }

def findCorrespondingLaggingBottom(leadingBottom, indexInAllBottoms, allBottoms, bottomsHeightThreshold, bottomsWidthThreshold):
    leadingIndex = leadingBottom["index"]
    leadingPrice = leadingBottom["value"]
    for i in range(indexInAllBottoms + 1, len(allBottoms)):
        laggingCandidatePrice = allBottoms[i]["value"]
        laddingCandidateIndex = allBottoms[i]["index"]
        if (
            1 >= laggingCandidatePrice / leadingPrice >= bottomsHeightThreshold 
            and laddingCandidateIndex + bottomsWidthThreshold <= leadingIndex
        ):
            return {"value": laggingCandidatePrice, "index": laddingCandidateIndex}
    return None
        
def findMidpoint(laggingBottom, leadingBottom, prices):
    subListLeftIndex = laggingBottom["index"] + 1
    subListRightIndex = leadingBottom["index"]
    subList = prices[subListLeftIndex:subListRightIndex]
    midPoint = {"value": subList[0], "index": subListLeftIndex}
    for i in range(len(subList)):
        price = subList[i]
        if price > midPoint['value']:
            midPoint = {"value": price, "index": i + laggingBottom["index"]}
    return midPoint
            
            
def findBreakout(leadingBottom, prices):
    startIndex = leadingBottom["index"]+1
    subList = prices[startIndex:]
    breakOut = {"value": subList[0], "index": startIndex}
    for i in range(len(subList)):
        price = subList[i]
        if price > breakOut['value']:
            breakOut = {"value": price, "index": i +  leadingBottom["index"]}
    return breakOut
    
def isEmpireTop(mid, left, right):
    return mid > right and mid > left

def isEmpireBottom(mid, left, right):
    return mid < right and mid < left
