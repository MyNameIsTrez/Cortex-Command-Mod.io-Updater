# Cortex-Command-Mod.io-Updater

Scripts used for downloading, converting, testing, and updating all [Cortex Command Community Project mods](https://mod.io/g/cccp/) automatically.

It is highly recommended that you drop `Benchmark.rte` from [my mod repository](https://github.com/MyNameIsTrez/Cortex-Command-Mods) into your game's `Mods/` directory, as it is ran for 60 seconds to verify nothing gets printed to the console, nor any crashes occur.

You'll also need to add this to your CCCP's `UserData/Settings.ini` in order for that `Benchmark.rte` to be used by the tester:

```ini
	LaunchIntoActivity = 1
	DefaultActivityType = GAScripted
	DefaultActivityName = Combat Benchmark
	DefaultSceneName = Benchmark
```

Use this to find mentions of `JetTime` that don't have `Jetpack.` in front of it:
`^(.*)?\b(?<!Jetpack\W)JetTime\b(.*)$`
And use this to put `Jetpack.` in front of it:
`$1Jetpack.JetTime$2`
given that we *only* don't want this first line to be matched:
```
print(Jetpack) print(Jetpack.JetTimeTotal) a
print(Jetpack.JetTimeTotal) print(foo.JetTimeTotal) a
print(Jetpack) print(foo.JetTimeTotal) a
print(bar) print(foo.JetTimeTotal) a
```
