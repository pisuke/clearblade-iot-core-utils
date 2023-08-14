package main

import (
	"context"
	"fmt"

	iot "github.com/clearblade/go-iot"
)

func deleteRegistry(projectID string, region string, registryID string) (*iot.Empty, error) {
	ctx := context.Background()
	service, err := iot.NewService(ctx)
	if err != nil {
		return nil, err
	}

	name := fmt.Sprintf("projects/%s/locations/%s/registries/%s", projectID, region, registryID)
	fmt.Println("name: ")
	fmt.Println(name)
	response, err := service.Projects.Locations.Registries.Delete(name).Do()
	if err != nil {
		return nil, err
	}

	fmt.Println("Deleted registry:")
        fmt.Println(registryID)
        return response, nil
}

func main() {

	// Test Delete a Registry
	res, err := deleteRegistry("PROJECT-NAME", "us-central1", "REGISTRY-NAME")
	if err != nil {
		fmt.Println("Error out")
		fmt.Println(err.Error())
	}

	fmt.Println(res)

}
