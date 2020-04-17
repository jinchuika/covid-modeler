import os
import sys
module_path = os.path.abspath(os.path.join('.'))
if module_path not in sys.path:
    sys.path.append(module_path)

from gooey import Gooey, GooeyParser

from modeler.wrapper import Modeler

@Gooey()
def main():
    parser = GooeyParser(description='Process some integers.')
    modeler = Modeler()

    parser.add_argument(
        'country',
        widget='Dropdown',
        choices=modeler.c.show_countries(),
        help='Select a country from the list'
    )

    # predict_len=15, use_default_models=True, mode='notebook', output_folder='output', plot_mode='image'

    parser.add_argument(
        '--predict_len',
        default=15,
        metavar='Prediction length',
        type=int,
        help='Days to predict from the last train date'
    )

    parser.add_argument(
        '--output_folder',
        default='output',
        metavar='Output folder',
        type=str,
        help='Where to put write the results'
    )

    parser.add_argument(
        '--show_plot',
        metavar='Show plot after finished',
        widget='Dropdown',
        choices=['Yes', 'No'],
        default='Yes',
        help='Show the plot after finishing'
    )

    args = parser.parse_args()
    print(args)
    show_plot = str(args.show_plot) == 'Yes'
    modeler = Modeler(
        country=args.country,
        predict_len=args.predict_len,
        output_folder=args.output_folder,
        mode='cli',
        plot_mode='html',
        show_plot=show_plot
    )
    modeler.process()


if __name__ == '__main__':
    main()
