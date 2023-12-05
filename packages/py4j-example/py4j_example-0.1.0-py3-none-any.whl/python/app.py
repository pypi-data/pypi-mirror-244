from py4j.java_gateway import JavaGateway
from py4j.java_collections import ListConverter


class ApplicationWrapper:
    """
    Initialize the object.

    This function is the constructor of the class and is called when a new object of the class is created.
    It initializes the `gateway` attribute by launching the Java gateway using the `launch_gateway` method
    from the `JavaGateway` class.
    The `jarpath` parameter is used to specify the path to the `py4j.jar` file,
    and the `classpath` parameter is used to specify the path to the `application.jar` file.
    Additionally, it initializes the `application` attribute by accessing the `Application` class
    from the `gateway.jvm.org.example.application` module.

    """
    def __init__(self):
        self.gateway = JavaGateway.launch_gateway(jarpath="/path/to/py4j-0.10.9.7.jar",
                                                  classpath="/path/to/Py4J-1.0-SNAPSHOT.jar")
        self.application = self.gateway.jvm.org.example.application.Application()

    def add(self, a, b):
        return self.application.add(a, b)

    def subtract(self, a, b):
        return self.application.subtract(a, b)

    def getArrayLength(self, lst):
        java_array = self.gateway.new_array(self.gateway.jvm.int, len(lst))
        for i in range(len(lst)):
            java_array[i] = lst[i]
        return self.application.getArrayLength(java_array)

    def getListLength(self, lst):
        java_list = ListConverter().convert(lst, self.gateway._gateway_client)
        return self.application.getListLength(java_list)
