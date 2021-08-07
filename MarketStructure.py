import math

def bottom(prices):
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
    bottomsHeightThreshold = 0.8
    bottomsWidthThreshold = math.floor(len(prices)/3) #bars
        
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
                            mid / leadingBottom['value']  >= bottomsHeightThreshold 
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
    )
        
    return {
        "state": state,
        "laggingBottomPrice": laggingBottom['value'] if laggingBottom is not None else None,
        "leadingBottomPrice": leadingBottom['value'] if leadingBottom is not None else None,
        "midPointPrice": midPoint['value'] if midPoint is not None else None,
        "breakoutPrice": breakout['value'] if breakout is not None else None,
    }
    
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
