#data set
day_analysis = read.csv("C:\\Users\\Home\\Desktop\\myAccount\\day_analysis_v2.csv",stringsAsFactors = FALSE)
hour_analysis = read.csv("C:\\Users\\Home\\Desktop\\myAccount\\hour_analysis_v2.csv",stringsAsFactors = FALSE)
hour_analysis['hour'] <-  lapply(hour_analysis['hour'], factor)
time_analysis = read.csv("C:\\Users\\Home\\Desktop\\myAccount\\time_analysis2_v2.csv",stringsAsFactors = FALSE)

#box plot
boxplot(withdrawal~day_of_week,data = day_analysis,  main="Boxplot of expenditure by day",
    xlab = "day", ylab = "expenditure(won)")

boxplot(withdrawal~hour,data = hour_analysis,  main="Boxplot of expenditure by date",
        xlab = "hour", ylab = "expenditure(won)")

#One-way ANOVA for day
out = aov(withdrawal~day_of_week,data = day_analysis)
summary(out)
anova(out)
#One-way ANOVA for hour
out2 = aov(withdrawal~hour,data = hour_analysis)
summary(out2)
anova(out2)


