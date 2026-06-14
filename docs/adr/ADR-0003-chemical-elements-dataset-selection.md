# ADR-0003: Chemical elements dataset selection

## Status

Accepted - 2026-06-14

## Context

Phase 1 requires designing the data model for the periodic table elements and the
strategy for migrations and seeding. Before any of that, it is essential and
high-priority to choose and fix the data source that the API will rely on.

To decide between the available data sources, the following criteria are applied:

1. **Licence (eliminatory):** the source must carry a valid licence with explicit
   permissions, compatible with the API's MIT licence. This criterion is a hard gate.
2. **Field suitability for the Spanish Secondary Education curriculum:** the source
   must provide, at minimum, the attributes used at secondary level (name, symbol,
   atomic number, atomic mass, atomic radius, electronegativity, ionisation energy,
   electron affinity and electron configuration) for all 118 elements of the periodic
   table.
3. **Consumption format:** a format that is simple for the API to ingest; CSV or JSON
   are preferred.
4. **Provenance:** sources originating from a recognised scientific authority are
   preferred.

This decision unblocks the data model and migration strategy decisions, detailed in
the upcoming ADR-0004 and ADR-0005.

## Decision

Based on the criteria above, the selected data source is the downloadable periodic
table in **CSV** format provided by **PubChem** (NLM/NCBI).

The dataset's provenance is authoritative and recognised, and its columns cover
the curriculum without unnecessary surplus. PubChem aggregates data from many
third-party sources whose individual copyright terms may vary, but the
periodic-table element data consumed here is produced by NLM/NCBI and is in the
public domain per the [NLM data usage policy](https://www.ncbi.nlm.nih.gov/home/about/policies/),
which imposes no redistribution restrictions on it.

A distinction is drawn between the **source of provenance** (PubChem/NCBI) and the
**vendored artefact** actually consumed by the seed process. The CSV is **vendored**
into the repository (e.g. under `data/raw/`) rather than downloaded at build time.
For a small, static dataset (118 rows), vendoring guarantees full reproducibility:
anyone cloning the repository obtains identical data without depending on the source
URL remaining stable over time, and the CI pipeline can seed the database without
external network access. Its public-domain status permits this redistribution
without friction.

The dataset is provided in English, whereas the application targets Spanish students.
The decision on the ES/EN localisation strategy is deferred to ADR-0004.

## Consequences

### Positive

- **Seed reproducibility:** relying on a fixed, vendored CSV with no external API
  dependency at build or runtime isolates the data layer from unexpected upstream
  changes and from network availability.
- **Scientific credibility:** an NCBI/PubChem source aligns with the rigour expected
  of an educational scientific project and can be cited as a reputable reference in
  the README.
- **Usage rights:** the public-domain status allows free use with no ShareAlike
  clause and no mandatory attribution. The NLM policy nonetheless requests
  acknowledgement of the source, which the project honours by crediting
  PubChem/NCBI in the README.

### Trade-offs

- **PUG-REST API complexity:** the PubChem programmatic API is comparatively complex
  and is set aside for the MVP in favour of the CSV. Should the project later require
  data not present in the CSV (e.g. isotopes), revisiting the API will be necessary.
- **Source last maintained in 2018:** although the dataset is not recently updated,
  chemical element data does not require ongoing supervision, as these values are
  stable physical constants rather than live data. When new elements are discovered
  or synthesised and added to the periodic table, the method for incorporating that
  low-volume data will be assessed in a future ADR.
- **Localisation pending:** the dataset contains English-language data. The
  localisation work is deferred to ADR-0004.

## Alternatives considered

- **Kaggle (mexwell, CC BY 4.0):** good licence and rich in fields, but discarded as
  the primary source because its provenance cannot be verified with the same
  authority as NCBI (a Kaggle dataset inherits the quality of its original source,
  which is not clearly documented here). Retained as a viable plan B if a required
  field proves to be missing from the PubChem CSV.
- **Bowserinator/Periodic-Table-JSON (CC BY-SA 3.0):** complete and widely used, but
  the ShareAlike clause imposes licensing obligations on derived data that add
  friction against the simplicity sought for the project's data layer.
- **periodictableofelements.org:** discarded due to the absence of an explicit
  licence ("free use" is not a licence), which creates legal uncertainty about
  redistributing the data in an open-source repository.
