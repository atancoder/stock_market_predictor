# plot each feature against the label
data <- read.csv("labeled_data.csv")
pe_ratio <- data$pe_ratio
market_cap <- data$market_cap
past_pct_change <- data$past_pct_change

labels <- data$label

plot(pe_ratio, labels, main = "PE Ratio vs. Label", xlab = "PE Ratio", ylab = "Label", xlim = c(-500, 500))
# seems like there's not much of a correlation, so it would make sense the weight for this is very low

limits <- boxplot.stats(market_cap)$stats[c(1, 5)]
plot(market_cap, labels, main = "PE Ratio vs. Label", xlab = "PE Ratio", ylab = "Label", xlim = limits)
# No correlation here either

limits <- boxplot.stats(past_pct_change)$stats[c(1, 5)]
plot(past_pct_change, labels, main = "PE Ratio vs. Label", xlab = "PE Ratio", ylab = "Label", xlim = limits)
# No correlation here either
