# Save output as pdf
pdf('charts.pdf')

# Download skirts.dat from the web
skirts <- scan("http://robjhyndman.com/tsdldata/roberts/skirts.dat",skip=5)

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

system('ls')

