# Save output as pdf
pdf('charts.pdf')

# Download skirts.dat from bucket
system("picloud bucket get skirts.dat .")

# Download skirts.dat from the web
skirts <- scan("skirts.dat",skip=5)

# Create timeseries
skirtsseries <- ts(skirts,start=c(1866))

# Plot raw data
plot.ts(skirtsseries)

# Smooth using Holt's exponential smoothing
skirtsseriesforecasts <- HoltWinters(skirtsseries, gamma=FALSE)
skirtsseriesforecasts
skirtsseriesforecasts$SSE

# Plot smoothed data
plot(skirtsseriesforecasts)

# Save output chart to bucket
system("picloud bucket put charts.pdf charts.pdf")
