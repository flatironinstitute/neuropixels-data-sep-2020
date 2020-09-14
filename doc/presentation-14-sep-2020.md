---
theme : "night"
transition: "slide"
highlightTheme: "monokai"
logoImg: ""
slideNumber: false
title: "neuropixels-data-sep-2020"
---

<style>
    .reveal section p {
      font-size: 0.7em;
    }
    .reveal section small {
      font-size: 0.4em;
    }
    .reveal section h3 {
      font-size: 0.8em;
    }
    .reveal section li {
      font-size: 0.6em;
    }
    .reveal a {
      font-size: 0.6em
    }
    img {
      border: black !important
    }
</style>

::: block
*neuropixels-data-sep-2020* {style=background:green;width:500px}
:::
::: block
*labbox-ephys* {style=background:green;width:500px}
:::

### Sharing of electrophysiology recordings and spike sorting results with web visualization and Python interface

Jeremy Magland and Jeff Soules<br />Center for Computational Mathematics, Flatiron Institute

---

### The value of shareable web links

<img width=80% src="https://i.imgur.com/NMhoj0P.png" />
<small>http://ephys1.laboratorybox.org/default/sorting/allen_mouse415148_probeE:curated?feed=sha1://7a471d097a5f084f2895298e8cca7be7e5def966/feed.json</small>

---

### The value of shareable web links

This recording has a noisy channel and a dead channel:

<img width=60% src="https://i.imgur.com/Il36bAA.png" />
<small>http://ephys1.laboratorybox.org/default/timeseriesForRecording/allen_mouse415148_probeE?feed=sha1://7a471d097a5f084f2895298e8cca7be7e5def966/feed.json</small>

---

### The value of shareable web links

The recording has a decent SNR for these channels:

<img width=60% src="https://i.imgur.com/6qxPTms.png">
<small>http://ephys1.laboratorybox.org/default/timeseriesForRecording/svoboda-SC026_080619_g0_tcat_imec2?feed=sha1://7a471d097a5f084f2895298e8cca7be7e5def966/feed.json</small>


---

### The value of shareable web links

These two units are probably a bursting pair and should be merged

<img src="https://i.imgur.com/vTFAw7t.png" />
<small>http://ephys1.laboratorybox.org/default/sortingUnit/svoboda-SC026_080619_g0_tcat_imec0:curated/20/?feed=sha1://7a471d097a5f084f2895298e8cca7be7e5def966/feed.json</small>

---

### The value of shareable web links

Example of slow drift

<img src="https://i.imgur.com/WU4corz.png" />
<small>http://ephys1.laboratorybox.org/default/sortingUnit/svoboda-SC026_080619_g0_tcat_imec2:curated/12/?feed=sha1://7a471d097a5f084f2895298e8cca7be7e5def966/feed.json</small>

<img src="https://i.imgur.com/A8sHSBK.png" />
<small>http://ephys1.laboratorybox.org/default/sortingUnit/svoboda-SC026_080619_g0_tcat_imec2:curated/28/?feed=sha1://7a471d097a5f084f2895298e8cca7be7e5def966/feed.json</small>

---

### SpikeForest

<img src="https://i.imgur.com/aI22Ahk.png" />
https://spikeforest.flatironinstitute.org

---

### The sha1:// URI

| |  |
| --- | --- |
| Raw .dat file | sha1://a3c889.../cortexlab-single-phase-3.dat |
| .npy file | sha1://889271.../clusterIds.npy |
| .mat file | sha1://7fd357.../curation.mat |
| Recording | sha1://b7efa1.../cortexlab-single-phase-3.json |
| Sorting | sha1://36706e.../cortexlab-single-phase-3-curated.json |
| Collection | sha1://4aea6a.../neuropix-recordings.json |
| Web link | http://ephys1.laboratorybox.org/default/sortingUnit/svoboda-SC026.../28/?feed=sha1://7a471d.../feed.json |

---

### Prepare datasets scripts (universally runnable)

<img src="https://i.imgur.com/jG60jIt.png" />
https://github.com/flatironinstitute/neuropixels-data-sep-2020

---

### Prepare datasets scripts (universally runnable)

<img src="https://i.imgur.com/LNKzjtZ.png" />

---

### Content-addressing => decentralized

* When files are addressed via content-dependent URIs, we are not tied to any particular mechanism for hosting the data
* Thus we can easily swap between centralized and decentralized 
* Centralized archives are great, but there are times when a decentralized or distributed approach offers an advantage

<img src="https://upload.wikimedia.org/wikipedia/commons/4/40/Categor%C3%ADas_de_ANT.jpg">

---

### Advantages of decentralized sharing of ephys

* Raw recordings (TB of data) -- sometimes it makes the most sense for them to reside in the lab where they were collected
* Burden of hosting (BW + disk) shared between producers and consumers
* One lab using huge resources does not impede on another lab
* There is more enough disk space / compute power to go around, if it is done cooperatively
* Store data if it is important to you
* Popular datasets are automatically replicated (like BitTorrent)

<img src="https://i.imgur.com/u17qdcW.png" width=500>

---

### I was inspired by the dat protocol

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Dat-data-logo-2017.svg/128px-Dat-data-logo-2017.svg.png" width=50 />

<q>...The Web uses a centralized data model optimized for use by commercial organizations... A siloed, centralized data preservation model benefits entities that manage, monetize, and gate-keep access to information. This model disincentivizes cooperative infrastructure for sharing information and does not prioritize data access or preservation.</q>

<q>We believe that introducing decentralization at an infrastructural level will allow existing silos (institutional data repositories, third party data preservation platforms) to share information, making data easier to access, improving redundancy, and forming the basis of a cooperatively run data preservation network.</q>

Robinson, Danielle C., et al. "The Dat Project, an open and decentralized research data tool." Scientific data 5.1 (2018): 1-4.

---

Why did we make something new instead of using

IPFS, BitTorrent, dat, etc..?

<nobr>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Ipfs-logo-1024-ice-text.png/440px-Ipfs-logo-1024-ice-text.png" width=100 />
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/7/7a/Application-x-bittorrent.svg/1024px-Application-x-bittorrent.svg.png" width=100 />
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Dat-data-logo-2017.svg/128px-Dat-data-logo-2017.svg.png" width=100 />
</nobr>

---

### Ideally, we want to do this:

```python
# Share a recording
import something as s

# Lazy-load recording from local disk (SpikeInterface)
recording = ... 
uri = s.share_recording(recording)

# print unique URI and e-mail to colleague
print(uri)
```

```python
# Our colleague loads the recording
import something as s
# Lazy-load recording from remote computer (p2p network)
recording = s.load_recording('sha1://content-determined-hash')

# data flows directly between the peers
traces = X.raw_traces(start_frame=0, end_frame=100000)
```

* No login / authentication
* No upload
* No central server
* No file format concerns

---

### Or share spike sorting visualization via web

```python
import something as s

recording = ... # load recording from disk
sorting = ... # load spike sorting from disk

url = s.prepare_web_visualization(recording, sorting)

# print web URL and send to colleague
print(url)
```

* No software installation for viewer
* No central data server (except web page server)

---

### Kachery-p2p: how it works

<img src="https://i.imgur.com/uSg5l0J.png" width=80% />
<small>https://github.com/flatironinstitute/kachery-p2p</small>

---

### Kachery-p2p: how it works

<img src="https://i.imgur.com/luzdcgL.png?1" />
<small>https://github.com/flatironinstitute/kachery-p2p</small>

---

### Separation of concerns

<img src="https://i.imgur.com/UXqyryB.png?1">

---

### Other topics

* Submitting new recordings / sortings
* Remote compute resources
* Comparison between sortings
* Plugin metrics
* Improved kachery-p2p protocol

---

### Thank you

* **Organizing the workshop**: Karel, Ken, Laura, Alyssa
* **Datasets**: Susu Chen, Nick Steinmetz, Josh Siegle
* **Troubleshooting kachery-p2p**: Pierre Yger, Alex Morley
* **SpikeInterface**: Matthias Henng, Cole Hurwitz, Alessio Buccino, Samuel Garcia
* **Help with Labbox-ephys**: Fan Wu (DiagnosticBiochips)
* **At Flatiron**: Jeff Soules, Alex Barnett, Leslie Greengard