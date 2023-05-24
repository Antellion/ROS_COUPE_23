import launch
import launch_ros.actions

def generate_launch_description():
    return launch.LaunchDescription([
        launch_ros.actions.Node(
                package='coupe',
                executable='Lidar',
                name='Lidar'
        ),
        launch_ros.actions.Node(
                package='coupe',
                executable='master',
                name='master'
        ),
        launch_ros.actions.Node(
                package='coupe',
                executable='moteur',
                name='moteur'
        ),
        launch_ros.actions.Node(
                package='coupe',
                executable='actionneur',
                name='actionneur'
        ),
        launch_ros.actions.Node(
        	package='idh',
        	executable='idh',
        	name='idh'
        )
    ])
