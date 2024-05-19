FROM mcr.microsoft.com/dotnet/sdk:8.0
WORKDIR /App

ENV FLAG="CSCG{TESTFLAG}"
# Copy everything
COPY PhotoEditor/ ./
# Restore as distinct layers
RUN dotnet restore
# Build and publish a release
ENTRYPOINT ["bash", "-c", "echo $FLAG > ./flag && dotnet run --urls=http://0.0.0.0:1024"]