## Estado 
Aceptada — 2026-05-24 
## Contexto
Durante el desarrollo del proyecto se tomarán decisiones técnicas significativas (elección de stack, patrones de arquitectura, librerías, estrategias de despliegue) que afectarán al diseño a largo plazo. Sin un registro estructurado, estas decisiones se pierden o se reinterpretan con el tiempo, dificultando la incorporación de nuevos colaboradores y la revisión retrospectiva. 
## Decisión
Se adoptará el formato ADR (Architecture Decision Record) propuesto por Michael Nygard para documentar toda decisión arquitectónica relevante. Los ADRs: 
- Se almacenarán en `/docs/adr/` dentro del repositorio. 
- Seguirán la nomenclatura `NNNN-titulo-en-kebab-case.md`. 
- Serán inmutables una vez aceptados: si una decisión cambia, se crea un nuevo ADR que reemplaza al anterior (estado: "Reemplazada por ADR-NNNN"). 
- Tendrán las secciones: Estado, Contexto, Decisión, Consecuencias, Alternativas consideradas. 
## Consecuencias 
**Positivas** 
- Trazabilidad histórica de las decisiones técnicas. 
- Onboarding más rápido para futuros colaboradores. 
- Refuerza el pensamiento estructurado antes de decidir. 
**Negativas** 
- Sobrecarga de tiempo en la redacción. 
- Riesgo de inflación documental si se abusa del formato. 
## Alternativas consideradas 
- **Wiki en GitHub:** descartada por desacoplamiento del código. 
- **Comentarios en commits:** descartada por baja visibilidad. 
- **No documentar:** descartada por pérdida de contexto a largo plazo.