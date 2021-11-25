# Quantum Key Distribution

This project is about Quantum Key Distribution (QKD).\
It is divided into the following packages:

- a [Quantum Channel Simulator (QCS)](qcs/README.md)
- a [Key Management Entity (KME)](kme/README.md)
- a [Key Manager](key_manager/README.md)

In summary, QCS receives requests from applications that want to use quantum-generated secret keys. QCS is a simulator
of a quantum channel that produces quantum secret keys. The key manager stays between the two previous entities.

**Attention**: this is only a draft of the entire project. The definition, the division and also the name chosen for
each package may change in the future.

## Sources

- https://www.etsi.org/committee/1430-qkd

## People

- [Nicolò Sala](mailto:nicolo4.sala@mail.polimi.it), graduate student
- [Paolo Martelli](mailto:paolo.martelli@polimi.it), supervisor
- [Marco Brunero](mailto:marco.brunero@polimi.it), project contact person
- [Alberto Gatto](mailto:alberto.gatto@polimi.it), project contact person
