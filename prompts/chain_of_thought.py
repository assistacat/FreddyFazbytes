chain_of_thoughts_prompt = """
We are building a review filtering system to intentionally remove unhelpful content so that only useful,
trustworthy, and policy-compliant reviews remain. Irrelevant, misleading, or low-quality reviews can distort
public perception of a business; your task is to reason carefully and classify each review.

Think step by step like a human reviewer:
1. Read the review carefully and examine its content.
2. Look at the metadata (review length, posting time, user history, keywords, links, etc.).
3. Consider whether the review provides useful, verifiable information about the business or location.
4. Ignore star ratings when judging quality, since most reviews are ★5 and ratings alone are unreliable.
5. Decide the category of the review:
   - Ad: Promotional content, discounts, links, marketing intent.
   - Irr: Irrelevant, vague, unhelpful (e.g., one-word comments, pure emotion with no detail).
   - Rant: Excessively negative, emotional venting without constructive details.
   - Val: Valid, meaningful, and informative review.
6. Assign a Relevancy Score from 0 to 1:
   - 1 = Highly useful, trustworthy, and informative
   - 0 = Spam, misleading, or irrelevant
7. Flag if the review violates policy (contains links, profanity, spam indicators, etc.).
8. Give the final output.

---

### Example 1
Review: “This café has the best waffles ever! Come get 2-for-1 at www.wafflepromo.com”
Metadata:
 • Rating: 5
 • Store: “49 SEATS”
 • Reviewer: Hannah Eva
 • Review Length: 17 words
 • Sentiment: 0.9
 • Keywords Found: “2-for-1”, “promo”, “link”
 • Time Posted: 2:14 PM
 • Has Link: Yes
 • Profanity Detected: No
 • User History: 3 past reviews

Reasoning: The review contains a URL, promotional wording (“2-for-1”, “promo”), and marketing language rather than a genuine experience. The sentiment is overly positive but lacks details about food or service. Looks like an advertisement.
Category: Ad  
Relevancy Score: 0.1  
Flag Policy Violation: Yes  

---

### Example 2
Review: “Terrible place. Wouldn’t recommend at all.”
Metadata: Rating: 1 | Store: Coffee Corner | Reviewer: Jiayi

Reasoning: Very negative but vague. Doesn’t specify what aspect was terrible (food, service, price, atmosphere). Reads more like emotional venting than constructive feedback. Insufficient details to be useful.
Category: Irr  
Relevancy Score: 0.2  
Flag Policy Violation: Yes  

---

### Example 3
Review: “Very nice”
Metadata: Rating: 5 | Store: Sushi House | Reviewer: Amir

Reasoning: Review is short and vague, but not harmful or misleading. It expresses a genuine (though minimal) sentiment. Doesn’t provide much detail, so it’s only somewhat useful. Star rating ignored when judging quality.
Category: Val  
Relevancy Score: 0.5  
Flag Policy Violation: No  

---

### Example 4
Review: “Comforting, tasty food for supper at affordable prices, great service as well! 10% off after 10pm, and no service charge”
Metadata: Rating: 4 | Store: Happy Noodles | Reviewer: Sarah

Reasoning: Although it mentions a discount (10% off), the main content is about the food and service. It reflects a genuine dining experience (comforting food, affordable, great service). The promotional detail seems incidental and part of real experience, not marketing. Overall useful.
Category: Val  
Relevancy Score: 0.9  
Flag Policy Violation: No  

---
### Example 5
Review: "Never been here, but my friend said it’s terrible. Avoid!"
Metadata: Rating: 1 | Store: Burger Bay | Reviewer: Kenny

Reasoning: States no visit; relies on hearsay; no concrete details. Violates “no rant without visit evidence.” IGNORE star rating.
Category: Rant
Relevancy Score: 0.20
Flag Policy Violation: Yes

---

### Example 6
Review: “Bubble tea here sucks. each a cup is btr”
Metadata: Rating: 2 | Store: Boba Life | Reviewer: Darren
Reasoning: Negative review framed as a comparison to another brand. Dismissive, doesn’t provide constructive detail. Also promotional to competitor → resembles advertising/brand attack.
Category: Ad
Relevancy Score: 0.2
Flag Policy Violation: Yes

---

Now classify this new review:

Review: {clean_text}
Metadata: Rating: {rating} | Store: {store_name} | Reviewer: {reviewer_name} | Review Length: {review_length} | Sentiment: {sentiment} | Keywords: {keywords} | Time Posted: {time_posted} | Has Link: {has_link} | Profanity: {profanity_detected} | User History: {user_history}

Reasoning:
Category:
Relevancy Score:
Flag Policy Violation:
"""